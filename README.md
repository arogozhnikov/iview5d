# iview5d (stack viewer)

Extremely simplistic viewer of small ndimensional patches for jupyter notebooks. 
Powered by einops transformation

## Installation

Right from github
```
pip install git+ssh://git@github.com/arogozhnikov/iview5d.git
```

## Usage (viewing)

Move your cursor over the image - as you move 

## Usage (code)

First arument is tensor or list of tensors (from any framework)
Second argument corresponds to einops transformation pattern.

Output should have 4 or 5 dimensions in the following order

- x-controllable (changed by moving a mouse over the image)
- y-controllable (changed by moving a mouse over the image)
- height
- width
- (optional) color

In example below:

```
view5d(
    stack,
    'batch z channel h w -> batch z h w channel', 
    zoom=0.5,
)
```

Axes will be used as:
- batch -> move cursor along x
- z -> move cursor along y
- h w channel - shown image (at each position of cursor)


## Video 

See in action: 

## Try it out (demonstration)



## Warning

No additional features are planned for this project, it is designed to be small and convenient.
If you need fully-powered stack viewer - find a corresponding project 
  