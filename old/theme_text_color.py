# convert hex colors to integer
# adapted to python from: https://24ways.org/2010/calculating-color-contrast/

def get_contrast_yiq(hex_color):
    """ get contrasting black or white text color for a hex color """
    # convert hex to rbg
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    # scale according to visual impact compare to middle
    yiq = ((r*299)+(g*587)+(b*114))//1000
    if yiq >= 128:
        return '#000000' # black
    else:
        return '#FFFFFF' # white

# add a constrasting color to each theme in the color_hunt dictionary
from color_themes import *
for key, val in color_hunt.items():
    prime = val[0]
    text_color = get_contrast_yiq(prime)
    color_hunt[key] = val + (text_color,)

# export new colors with contrasting text color
with open('colors_new.py','w') as f:
    f.write('themes = {\n')
    for key, val in color_hunt.items():
        f.write(f"\t'{key}': {val},\n")
    f.write('}')