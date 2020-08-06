# iview5d

Extremely simplistic viewer of small ndimensional patches for jupyter notebook. Powered by einops

## Installation

Right from github
```
pip install git+ssh://git@github.com/arogozhnikov/iview5d.git
```

## Usage (viewing)

Move your cursor over the image.

## Code

Second argument corresponds to einops transformation pattern.

Output should have 4 or 5 dimensions in the following order

- x-controllable (changed by moving a mouse over the image)
- y-controllable (changed by moving a mouse over the image)
- height
- width
- optional color

In example below:
 
- changing  

```
view5d(
    stack,
    'deconvolved z h w -> () z h w deconvolved', 
    zoom=0.5,
)
```

