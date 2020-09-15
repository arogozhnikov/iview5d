import base64
from io import BytesIO

import numpy as np
from IPython.display import display_html
from einops import rearrange, asnumpy
from einops.einops import ParsedExpression
from matplotlib import pyplot as plt


def get_background_image_code(image, max_tolerable_size_in_bytes=20_000_000):
    with BytesIO() as myio:
        # TODO better compression?
        plt.imsave(myio, image, format='jpeg', cmap='gray')
        png_bytes = myio.getvalue()
    png_bytes_64 = base64.b64encode(png_bytes).decode()
    print('Size of an image: ', len(png_bytes_64) // 1000, 'kB')
    if len(png_bytes_64) > max_tolerable_size_in_bytes:
        raise RuntimeError('image is too large, try to pick a smaller fragment')
    return f'background-image: url(data:image/jpeg;base64,{png_bytes_64});'


def prepare_html_code(tensor, x_axis_name, y_axis_name, zoom=2):
    x_steps, y_steps, h, w = tensor.shape[:4]
    image = rearrange(tensor, 'x y h2 w2 ... -> (y h2) (x w2) ...')
    h *= zoom
    w *= zoom
    # keeping stuff in css variables (alternatively could use data-properties)
    style = f'''
        margin: 20px;
        height: {h}px; 
        width: {w}px; 
        --x-step: 0;
        --y-step: 0;
        --x-steps: {x_steps};
        --y-steps: {y_steps};
        --x-step-size: {w};
        --y-step-size: {h};
        --x-name: {x_axis_name};
        --y-name: {y_axis_name};
        {get_background_image_code(image)}
        background-size: {x_steps * w}px {y_steps * h}px;
        background-repeat: no-repeat;
        margin: 1px black;
        color: white;
        text-shadow: black 0px 0px 10px; /* does not work because of layering */
    '''

    onmousemove = '''
    (function(that){
        that.onmousemove = function(e) {
            div = e.target;
            var rect = e.target.getBoundingClientRect();
            var x = e.clientX - rect.left; //x position within the element
            var y = e.clientY - rect.top;  //y position within the element

            var x_steps     = div.style.getPropertyValue('--x-steps');
            var y_steps     = div.style.getPropertyValue('--y-steps');
            var x_step_size = div.style.getPropertyValue('--x-step-size');
            var y_step_size = div.style.getPropertyValue('--y-step-size');
            var prev_x_step = div.style.getPropertyValue('--x-step');
            var prev_y_step = div.style.getPropertyValue('--y-step');

            var x_step = Math.max(Math.min(Math.floor((x / rect.width)  * x_steps), x_steps - 1), 0); 
            var y_step = Math.max(Math.min(Math.floor((y / rect.height) * y_steps), y_steps - 1), 0);
            // stop if shown segment did not change
            if ((x_step == prev_x_step) && (y_step == prev_y_step)) return;

            div.style.setProperty('--x-step', x_step);
            div.style.setProperty('--y-step', y_step);

            div.style.backgroundPositionX = - x_step * x_step_size + 'px';
            div.style.backgroundPositionY = - y_step * y_step_size + 'px';
            var x_name = div.style.getPropertyValue('--x-name');
            var y_name = div.style.getPropertyValue('--y-name');

            var new_text = '';
            if (x_steps > 1) 
                new_text += x_name + '=' + (x_step + 1) + '/' + x_steps + ' ';
            if (y_steps > 1)
                new_text += y_name + '=' + (y_step + 1) + '/' + y_steps;
            div.innerHTML = new_text;
        }
    })(this);
    '''

    return f'<div style="{style}" onmousemove="{onmousemove}" > </div>'


def iview5d(tensor, einops_pattern, zoom=1, **axes_sizes):
    reshaped = rearrange(tensor, einops_pattern, **axes_sizes)
    reshaped = asnumpy(reshaped)
    assert len(reshaped.shape) in [4, 5], \
        'reshaped tensor should have 4 or 5 axes [y-controllable, x-controllable, height, width, color (optional)]'
    if len(reshaped.shape) == 5:
        assert reshaped.shape[-1] <= 3, 'number of colors should be less than 3'
        if reshaped.shape[-1] == 2:
            # pad to 3 colors, fill last channel with zeros
            reshaped = np.pad(reshaped, [(0, 0), (0, 0), (0, 0), (0, 0), (0, 1)], mode='constant')
        elif reshaped.shape[-1] == 1:
            reshaped = reshaped[:, :, :, :, 0]

    parsed_right_part = ParsedExpression(einops_pattern.split('->')[1]).composition
    x_name = ','.join(parsed_right_part[0])
    y_name = ','.join(parsed_right_part[1])

    rendered = prepare_html_code(reshaped, zoom=zoom, x_axis_name=x_name, y_axis_name=y_name)
    display_html(rendered, raw=True)
