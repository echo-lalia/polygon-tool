import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

"""
This is a tool to help create polygon definitions for MicroPythons 'FrameBuffer.polygon' method,
(and for any other code that needs a simple list of coordinates to define a polygon.)

The intended use is for creating vector 'icons' that can be used in MicroPython programs.
"""

# initial config: 

WIDTH = 32
HEIGHT = 32

PX_SIZE = 15

CANVAS_WIDTH = WIDTH * PX_SIZE
CANVAS_HEIGHT = HEIGHT * PX_SIZE

INDENTATION = "    "
UI_CLR_TEXT = "CONFIG['ui_color']"
BG_CLR_TEXT = "CONFIG['bg_color']"

OUTPUT_PREFIX = "my_shape = (\n"
OUTPUT_SUFFIX = INDENTATION + ")"

UI_COLOR = 0
BG_COLOR = 1

OFFSET_X = 0
OFFSET_Y = 0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBALS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DEFAULT_ACTION = {
    "name":"poly",
    "coords":[],
    "color":UI_COLOR,
    "fill":False,
}

TOTAL_SHAPE = []

POLYCOORDS = []
CURRENT_ACTION = DEFAULT_ACTION.copy()


IMAGE = Image.new(mode='1', size=(WIDTH,HEIGHT), color=1)
WINDOW = tk.Tk()
CANVAS_IMG = None
PHOTO_IMG = ImageTk.PhotoImage(image='RGB', size=(CANVAS_WIDTH,CANVAS_HEIGHT))
DRAW = ImageDraw.Draw(IMAGE)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TKINTER OBJECTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

title = tk.Label(
    text="Polygon Maker",
    width=50)
title.pack()

OPTIONS_FRAME = tk.Frame(
    master=WINDOW,
)
OPTIONS_FRAME.pack()

PIXEL_FRAME = tk.Frame(
    master=WINDOW,
    borderwidth=5,
    relief=tk.RAISED
)
PIXEL_FRAME.pack(side=tk.LEFT)

CONTROL_FRAME = tk.Frame(
    master=WINDOW,
    borderwidth=5,
)
CONTROL_FRAME.pack(side=tk.RIGHT)

CREATE_FRAME = tk.Frame(
    master=CONTROL_FRAME,
    borderwidth=5,
)
CREATE_FRAME.pack()
CREATE_FRAME.columnconfigure([0, 1], minsize=200)
CREATE_FRAME.columnconfigure(2, minsize=50)


CANVAS = tk.Canvas(master=PIXEL_FRAME, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
CANVAS.pack(side=tk.LEFT, expand=True)

CANVAS_IMG = CANVAS.create_image((CANVAS_WIDTH//2,CANVAS_HEIGHT//2),anchor='center',image=PHOTO_IMG)
PHOTO_IMG.paste(IMAGE.resize((CANVAS_WIDTH,CANVAS_HEIGHT)))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEFINE BUTTONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# options
WIDTH_LABEL = tk.Label(
    master=OPTIONS_FRAME,
    text='Width:'
)
WIDTH_ENTRY = tk.Entry(
    master=OPTIONS_FRAME,
    width=5,
)

HEIGHT_LABEL = tk.Label(
    master=OPTIONS_FRAME,
    text='Height:'
)
HEIGHT_ENTRY = tk.Entry(
    master=OPTIONS_FRAME,
    width=5,
)

PX_SIZE_LABEL = tk.Label(
    master=OPTIONS_FRAME,
    text='Pixel size:'
)
PX_SIZE_ENTRY = tk.Entry(
    master=OPTIONS_FRAME,
    width=5,
)
WIDTH_LABEL.grid(column=0, row=0)#, sticky=tk.E)
WIDTH_ENTRY.grid(column=1, row=0)#, sticky=tk.W)
HEIGHT_LABEL.grid(column=3, row=0)#, sticky=tk.E)
HEIGHT_ENTRY.grid(column=4, row=0)#, sticky=tk.W)
PX_SIZE_LABEL.grid(column=6, row=0)#, sticky=tk.E)
PX_SIZE_ENTRY.grid(column=7, row=0)#, sticky=tk.W)

WIDTH_ENTRY.insert(0, str(WIDTH))
HEIGHT_ENTRY.insert(0, str(HEIGHT))
PX_SIZE_ENTRY.insert(0, str(PX_SIZE))

for i in range(0,8):
    OPTIONS_FRAME.columnconfigure(i, weight=1, minsize=24)

def handle_update_options(event):
    global PX_SIZE, WIDTH, HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, PHOTO_IMG, CANVAS_IMG, IMAGE, DRAW
    if event.keysym == 'Return':
        try:
            PX_SIZE = int(PX_SIZE_ENTRY.get())
        except:
            PX_SIZE = 15
            PX_SIZE_ENTRY.delete(0, tk.END)
            PX_SIZE_ENTRY.insert(0, str(PX_SIZE))
            gui_print("Couldn't parse pixel size.")
        try:
            WIDTH = int(WIDTH_ENTRY.get())
        except:
            WIDTH = 32
            WIDTH_ENTRY.delete(0, tk.END)
            WIDTH_ENTRY.insert(0, str(WIDTH))
            gui_print("Couldn't parse width.")
        try:
            HEIGHT = int(HEIGHT_ENTRY.get())
        except:
            HEIGHT = 32
            HEIGHT_ENTRY.delete(0, tk.END)
            HEIGHT_ENTRY.insert(0, str(HEIGHT))
            gui_print("Couldn't parse height.")

    # update all values and redraw
    CANVAS_WIDTH = WIDTH * PX_SIZE
    CANVAS_HEIGHT = HEIGHT * PX_SIZE

    IMAGE = IMAGE.resize((WIDTH, HEIGHT))
    DRAW = ImageDraw.Draw(IMAGE)

    PHOTO_IMG = ImageTk.PhotoImage(image='RGB', size=(CANVAS_WIDTH,CANVAS_HEIGHT))
    CANVAS_IMG = CANVAS.create_image((CANVAS_WIDTH//2,CANVAS_HEIGHT//2),anchor='center',image=PHOTO_IMG)
    PHOTO_IMG.paste(IMAGE.resize((CANVAS_WIDTH,CANVAS_HEIGHT)))
    CANVAS.config(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

    rule_lines()
    draw_image_on_canvas()
    format_print_shape()

PX_SIZE_ENTRY.bind("<Key>", handle_update_options)
WIDTH_ENTRY.bind("<Key>", handle_update_options)
HEIGHT_ENTRY.bind("<Key>", handle_update_options)


# MAIN BUTTONS

# create foreground polygon
def handle_create_poly_fg(event):
    global CURRENT_ACTION
    if CURRENT_ACTION['coords']:
        TOTAL_SHAPE.append(CURRENT_ACTION)

    CURRENT_ACTION = DEFAULT_ACTION.copy()
    CURRENT_ACTION['coords'] = []
    #gui_print(f"{TOTAL_SHAPE} \n {CURRENT_ACTION}")
    format_print_shape()

POLY_FG_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Create Polygon (Foreground)',
    background='lavender',
    activebackground='darkorchid',
    activeforeground='floralwhite'
)
POLY_FG_BUTTON.grid(column=0, row=0, sticky=tk.W)
POLY_FG_BUTTON.bind("<Button>", handle_create_poly_fg)




# create foreground filled poly
def handle_create_fill_fg(event):
    global CURRENT_ACTION
    if CURRENT_ACTION['coords']:
        TOTAL_SHAPE.append(CURRENT_ACTION)

    CURRENT_ACTION = DEFAULT_ACTION.copy()
    CURRENT_ACTION['fill'] = True
    CURRENT_ACTION['coords'] = []
    #gui_print(f"{TOTAL_SHAPE} \n {CURRENT_ACTION}")
    format_print_shape()

FILL_FG_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Create Filled Polygon (Foreground)',
    background='lavender',
    activebackground='darkorchid',
    activeforeground='floralwhite'
)
FILL_FG_BUTTON.grid(column=0, row=1, sticky=tk.W)
FILL_FG_BUTTON.bind("<Button>", handle_create_fill_fg)



# create background poly
def handle_create_poly_bg(event):
    global CURRENT_ACTION
    if CURRENT_ACTION['coords']:
        TOTAL_SHAPE.append(CURRENT_ACTION)

    CURRENT_ACTION = DEFAULT_ACTION.copy()
    CURRENT_ACTION['color'] = BG_COLOR
    CURRENT_ACTION['coords'] = []
    #gui_print(f"{TOTAL_SHAPE} \n {CURRENT_ACTION}")
    format_print_shape()

POLY_BG_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Create Polygon (background)',
    background='lavender',
    activebackground='darkorchid',
    activeforeground='floralwhite'
)
POLY_BG_BUTTON.grid(column=0, row=2, sticky=tk.W)
POLY_BG_BUTTON.bind("<Button>", handle_create_poly_bg)



# create filled bg poly
def handle_create_fill_bg(event):
    global CURRENT_ACTION
    if CURRENT_ACTION['coords']:
        TOTAL_SHAPE.append(CURRENT_ACTION)

    CURRENT_ACTION = DEFAULT_ACTION.copy()
    CURRENT_ACTION['color'] = BG_COLOR
    CURRENT_ACTION['fill'] = True
    CURRENT_ACTION['coords'] = []
    #gui_print(f"{TOTAL_SHAPE} \n {CURRENT_ACTION}")
    format_print_shape()

FILL_BG_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Create Filled Polygon (background)',
    background='lavender',
    activebackground='darkorchid',
    activeforeground='floralwhite'
)
FILL_BG_BUTTON.grid(column=0, row=3, sticky=tk.W)
FILL_BG_BUTTON.bind("<Button>", handle_create_fill_bg)



# DELETE BUTTONS:

def handle_delete_button(event):
    global CURRENT_ACTION, TOTAL_SHAPE

    if TOTAL_SHAPE and not CURRENT_ACTION['coords']:
        TOTAL_SHAPE.pop(-1)

    CURRENT_ACTION['coords'] = []

    draw_image_on_canvas()
    format_print_shape()

DELETE_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Delete last item',
    background='lightgoldenrod1',
    activebackground='lightcoral',
)
DELETE_BUTTON.grid(column=1, row=3, sticky=tk.E)
DELETE_BUTTON.bind("<Button>", handle_delete_button)



def handle_delete_all(event):
    global CURRENT_ACTION, TOTAL_SHAPE

    TOTAL_SHAPE = []

    CURRENT_ACTION['coords'] = []

    draw_image_on_canvas()
    format_print_shape()

DELETE_ALL_BUTTON = tk.Button(
    master=CREATE_FRAME,
    text='Clear ALL',
    background='lightcoral',
    activebackground='red',
)
DELETE_ALL_BUTTON.grid(column=1, row=0, sticky=tk.E)
DELETE_ALL_BUTTON.bind("<Button>",handle_delete_all)


def handle_copy(event):
    WINDOW.clipboard_clear()
    WINDOW.clipboard_append(OUTPUT_BOX.get("1.0", tk.END))

COPY_BUTTON = tk.Button(master=CREATE_FRAME, text='Copy output')
COPY_BUTTON.grid(column=3, row=3, sticky=tk.E)
COPY_BUTTON.bind("<Button>", handle_copy)


OUTPUT_BOX = tk.Text(master=CONTROL_FRAME)
OUTPUT_BOX.pack()




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def rule_lines():
    # add rule lines to canvas
    for y in range(HEIGHT):
        CANVAS.create_line(
            (
                0,
                y*PX_SIZE,
                CANVAS_WIDTH,
                y*PX_SIZE,
            ),
            fill="Gray"
        )
    for x in range(WIDTH):
        CANVAS.create_line(
            (
                x*PX_SIZE,
                0,
                x*PX_SIZE,
                CANVAS_HEIGHT,
            ),
            fill="Gray"
        )

def gui_print(text):
    global output_box
    OUTPUT_BOX.delete("1.0", tk.END)
    OUTPUT_BOX.insert("1.0", text)

def format_print_shape():
    output = OUTPUT_PREFIX

    shape = TOTAL_SHAPE + [CURRENT_ACTION]
    for item in shape:
        if item['coords']:
            
            clr_txt = UI_CLR_TEXT if item['color'] == UI_COLOR else BG_CLR_TEXT
            
            coords_txt = str(item['coords']).replace('[','(').replace(']',')').replace(' ','')
            
            output += INDENTATION
            output += f"({OFFSET_X},{OFFSET_Y}, {coords_txt}, {clr_txt}, {item['fill']}),\n"
    
    output += OUTPUT_SUFFIX

    gui_print(output)

def click_handler(event):
    global DRAW
    # event also has x & y attributes
    if event.num == 1:
        gui_print(str(event))

    # draw image to canvas
    add_to_polygon(event)
    draw_image_on_canvas()
    format_print_shape()




def add_to_polygon(event):
    x = int((event.x / PX_SIZE))
    y = int((event.y / PX_SIZE ))
    CURRENT_ACTION['coords'] += [x,y]

# def add_line_at_mouse(event):
#     x = int((event.x / PX_SIZE))
#     y = int((event.y / PX_SIZE ))

#     if not POLYCOORDS:
#         POLYCOORDS.append([(x,y)])
#     elif len(POLYCOORDS[-1]) == 1:
#         POLYCOORDS[-1].append((x,y))
#     else:
#         POLYCOORDS.append([(x,y)])

#     DRAW.point((x,y), fill=0)

# def draw_lines():
#     for line in POLYCOORDS:
#         if len(line) == 2:
#             DRAW.line(line, fill=0)

def draw_image_on_canvas():
    global IMAGE, CANVAS, PHOTO_IMG
    
    DRAW.rectangle((0,0, WIDTH,HEIGHT), fill=BG_COLOR)

    for item in TOTAL_SHAPE + [CURRENT_ACTION]:
        if item['name'] == 'poly':

            if len(item['coords']) == 2:
                DRAW.point(item['coords'], fill=item['color'])
            elif len(item['coords']) > 2:
                DRAW.polygon(
                    item['coords'],
                    fill= item['color'] if item['fill'] else None,
                    outline= item['color']
            )

    PHOTO_IMG.paste(IMAGE.resize((CANVAS_WIDTH,CANVAS_HEIGHT)))



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rule_lines()
CANVAS.bind("<Button>", click_handler)



WINDOW.mainloop()