import PySimpleGUI as sg
from themes_dict_11142019_2 import themes

# ----- THEME TESTER ---------------------------------------------------------
def add_theme(name, colors, table):
    """ add a new theme to the look and feel dict """
    theme = {
        'BACKGROUND': colors[0][0],
        'TEXT': colors[0][1],
        'INPUT': colors[2][0],
        'TEXT_INPUT': colors[2][1],
        'SCROLL': colors[1][0],
        'BUTTON': (colors[3][1], colors[3][0]),
        'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
        'PROGRESS_DEPTH': 0,
        'BORDER': 1,
        'SLIDER_DEPTH': 0,
        'TAGS': colors[4]
        }
    return theme


def get_contrast_yiq(hex_color):
    """ get contrasting black or white text color for a hex color """
    try:
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
    except:
        return '#FFFFFF'


def get_colors_from_theme(theme):
    colors = sg.LOOK_AND_FEEL_TABLE[theme]
    c1 = colors['BACKGROUND']
    c2 = colors['SCROLL']
    c3 = colors['INPUT']
    c4 = colors['BUTTON'][1]
    t1 = get_contrast_yiq(c1)
    t2 = get_contrast_yiq(c2)
    t3 = get_contrast_yiq(c3)
    t4 = get_contrast_yiq(c4)
    return [(t1, c1), (t2, c2), (t3, c3), (t4, c4)]

header_text1 = {
    'justification': 'center', 
    'font': (sg.DEFAULT_FONT, 10, 'bold'), 
    'background_color': get_colors_from_theme('DarkBlue')[0][1],
    'text_color': get_colors_from_theme('DarkBlue')[0][0],
    'size': (11, 1),
    'pad': (3, 2)}

header_text2 = {
    'justification': 'center', 
    'font': (sg.DEFAULT_FONT, 10, 'bold'), 
    'background_color': get_colors_from_theme('DarkBlue')[0][1],
    'text_color': get_colors_from_theme('DarkBlue')[0][0],
    'size': (11, 1),
    'pad': (0, 2)}

buttons_1 = {
    'size': (11, 2),
    'border_width': 0,
    'pad': (3, 1)
}

buttons_2 = {
    'size': (11, 2),
    'border_width': 0,
    'pad': (0, 2)
}

def create_window(ix):
    colors = [sg.LOOK_AND_FEEL_TABLE['SystemDefault']]
    
    col1 = [
        [sg.Text('Theme Name', **header_text1), 
         sg.Text('Color 1', **header_text2), sg.Text('Color 2', **header_text2),
         sg.Text('Color 3', **header_text2), sg.Text('Color 4', **header_text2)]]
    
    col2 = []
    for theme in sg.list_of_look_and_feel_values()[ix:ix+100]:
        sg.change_look_and_feel(theme)
        colors = get_colors_from_theme(theme)
        row = ix
        col2.append([
            sg.Button(theme, key=theme, button_color=('black', sg.DEFAULT_BACKGROUND_COLOR), **buttons_1),
            sg.Button(colors[0][1], button_color=colors[0], **buttons_2),
            sg.Button(colors[1][1], button_color=colors[1], **buttons_2),
            sg.Button(colors[2][1], button_color=colors[2], **buttons_2),
            sg.Button(colors[3][1], button_color=colors[3], **buttons_2)])
        row +=1

    sg.change_look_and_feel('DarkBlue')
    
    col3 = [
        [sg.Button('Prev Page', size=(11, 1), key='PREV'), 
         sg.Button('Next Page', size=(10, 1), focus=True, key='NEXT')]]
    
    layout = [
        [sg.Column(col1)],
        [sg.Column(col2, vertical_scroll_only=True, scrollable=True, size=(500, 500))],
        [sg.Column(col3, justification='right', pad=(15, 5))]]

    return sg.Window('Color Palette', layout)


# add all the themes to the look and feel table
for name, colors in themes.items():
    table = sg.LOOK_AND_FEEL_TABLE
    sg.LOOK_AND_FEEL_TABLE[name] = add_theme(name, colors, table)


# ----- TEST GUI ------------------------------------------------------------------
def btn(name):
    """ create gui buttons with standard parameters """
    return sg.Button(name, size=(6, 1), pad=(1, 1), key=name.upper())

def test_gui(location):
    """ create media player gui to handle vlc media player output """
    layout = [
        [sg.Input(default_text='URL or Local Path:', size=(30, 1), key='SUBMIT_NEW'), btn('load')],
        [sg.Image(filename='default.png', size=(426, 240), key='VID_OUT')],
        [btn('previous'), btn('play'), btn('next'), btn('pause'), btn('stop')],
        [sg.Text('LOAD media to Start', size=(40, 2), justification='center', font=(sg.DEFAULT_FONT, 10), key='INFO')]]
    return sg.Window('Mini Player', layout, element_justification='center', location=location, finalize=True)

# starting index
ix = 30

# window positions
window = create_window(ix)
width, height = window.get_screen_size()
main_x = (width - 1070)//2
main_y= height//4
test_x = main_x + 567 + 15
test_y = main_y
window.Location = (main_x, main_y)

while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'NEXT':
        window.close()
        ix += 100
        window = create_window(ix)
        window.Location = (main_x, main_y)
    if event == 'PREV':
        if ix != 30:
            window.close()
            ix -= 100
            window = create_window(ix)
            window.Location = (main_x, main_y)
    else:
        try:
            test_window.close()
            sg.change_look_and_feel(event)
            test_window = test_gui([test_x, text_y])
        except:
            sg.change_look_and_feel(event)
            test_window = test_gui([test_x, test_y])