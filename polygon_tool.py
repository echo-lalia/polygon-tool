import tkinter as tk
import tkinter.filedialog
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

COORD_PREFIX = "array.array('h', "
COORD_SUFFIX = ')'

UI_COLOR = 0
BG_COLOR = 1

OFFSET_X = 0
OFFSET_Y = 0

TRACE_ALPHA = 100

PACKED_PREFIX = 'my_shape = '
UNPACK_HINT = f"""
# def unpack_shape(string):
#     unpacked = (
#         "shape=("
#         + string.replace(
#         'u', "{COORD_SUFFIX}),{UI_CLR_TEXT}"
#         ).replace(
#         'b', "{COORD_SUFFIX}),{BG_CLR_TEXT}"
#         ).replace(
#         'a', "({OFFSET_X},{OFFSET_Y},{COORD_PREFIX}("
#         ).replace(
#         't', ',True)'
#         ).replace(
#         'f', ',False)'
#         )
#         + ")"
#         )
#     exec(unpacked)
#     return shape
    """

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
WINDOW.title('Polygon Tool')
WINDOW.columnconfigure(0, weight=1)
WINDOW.columnconfigure(1, weight=10)
WINDOW.rowconfigure([0,1], weight=1)
WINDOW.rowconfigure([2,3], weight=2)

CANVAS_IMG = None
PHOTO_IMG = ImageTk.PhotoImage(image='RGB', size=(CANVAS_WIDTH,CANVAS_HEIGHT))
DRAW = ImageDraw.Draw(IMAGE)

BG_IMAGE = None
BG_PHOTO_IMAGE = None
CANVAS_BG_IMG = None

STICKY_ALL = tk.E + tk.W + tk.N + tk.S

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TKINTER OBJECTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OPTIONS_FRAME = tk.Frame(
    master=WINDOW,
#    bg='RED',

)
OPTIONS_FRAME.columnconfigure(list(range(10)), weight=1, minsize=1)
OPTIONS_FRAME.columnconfigure([3,9], weight=10) # prevent options from being spread out on large windows
OPTIONS_FRAME.rowconfigure([0,1], weight=1)
OPTIONS_FRAME.grid(column=0, row=0, columnspan=2, sticky=tk.N+tk.E+tk.W)

PIXEL_FRAME = tk.Frame(
    master=WINDOW,
    borderwidth=5,
    relief=tk.RAISED,
)
PIXEL_FRAME.grid(column=0, row=2, rowspan=2)
PIXEL_FRAME.columnconfigure(0, minsize=max(CANVAS_HEIGHT, CANVAS_WIDTH))

CREATE_FRAME = tk.Frame(
    master=WINDOW,
    borderwidth=5,
#    bg='BLUE'
)
CREATE_FRAME.grid(column=1, row=1, rowspan=3, sticky=STICKY_ALL)
CREATE_FRAME.columnconfigure([0, 2], weight=1)
CREATE_FRAME.columnconfigure(1, weight=2)
CREATE_FRAME.rowconfigure(list(range(8)), weight=1)#, minsize=10)
CREATE_FRAME.rowconfigure(5, weight=40)
CREATE_FRAME.rowconfigure(6, weight=40)


CANVAS = tk.Canvas(master=PIXEL_FRAME, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
CANVAS.grid(column=0, row=0, sticky=STICKY_ALL)

CANVAS_IMG = CANVAS.create_image((CANVAS_WIDTH//2,CANVAS_HEIGHT//2),anchor='center',image=PHOTO_IMG)
PHOTO_IMG.paste(IMAGE.resize((CANVAS_WIDTH,CANVAS_HEIGHT)))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEFINE BUTTONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# options
WIDTH_LABEL = tk.Label(
    master=OPTIONS_FRAME,
    text='Width:',
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
WIDTH_LABEL.grid(column=4, row=0, sticky=tk.E)#, sticky=tk.E)
WIDTH_ENTRY.grid(column=5, row=0, sticky=tk.W)#, sticky=tk.W)
HEIGHT_LABEL.grid(column=6, row=0, sticky=tk.E)#, sticky=tk.E)
HEIGHT_ENTRY.grid(column=7, row=0, sticky=tk.W)#, sticky=tk.W)
PX_SIZE_LABEL.grid(column=8, row=0, sticky=tk.E)#, sticky=tk.E)
PX_SIZE_ENTRY.grid(column=9, row=0, sticky=tk.W)#, sticky=tk.W)o

WIDTH_ENTRY.insert(0, str(WIDTH))
HEIGHT_ENTRY.insert(0, str(HEIGHT))
PX_SIZE_ENTRY.insert(0, str(PX_SIZE))


def handle_update_options(event):
    global PX_SIZE, WIDTH, HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, PHOTO_IMG, CANVAS_IMG, IMAGE, DRAW, BG_PHOTO_IMAGE, CANVAS_BG_IMG
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



def open_file_dialog(event):
    file_path = tk.filedialog.askopenfilename(title="Select an image file", filetypes=[("All files", "*.*")])
    if file_path:
        print(file_path)
        open_image_file(file_path)
    handle_update_options(event)

def open_image_file(file_path):
    global BG_IMAGE
    BG_IMAGE = Image.open(file_path).convert('RGBA')

def clear_image(event):
    global BG_IMAGE
    BG_IMAGE = None
    handle_update_options(event)

OPEN_IMAGE_LABEL = tk.Label(
    master=OPTIONS_FRAME,
    text='Trace image:',
)
OPEN_IMAGE_BUTTON = tk.Button(
    master=OPTIONS_FRAME,
    text='Open',
)
CLEAR_IMAGE_BUTTON = tk.Button(
    master=OPTIONS_FRAME,
    text='Clear',
)
OPEN_IMAGE_LABEL.grid(column=0, row=0, sticky=tk.E)
OPEN_IMAGE_BUTTON.grid(column=1, row=0, sticky=tk.W+tk.E)
CLEAR_IMAGE_BUTTON.grid(column=2, row=0, sticky=tk.W)
OPEN_IMAGE_BUTTON.bind("<Button>", open_file_dialog)
CLEAR_IMAGE_BUTTON.bind("<Button>", clear_image)

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
DELETE_BUTTON.grid(column=2, row=3, sticky=tk.E)
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
DELETE_ALL_BUTTON.grid(column=2, row=0, sticky=tk.E)
DELETE_ALL_BUTTON.bind("<Button>",handle_delete_all)


def handle_copy(event):
    WINDOW.clipboard_clear()
    WINDOW.clipboard_append(OUTPUT_BOX.get("1.0", tk.END))

COPY_BUTTON = tk.Button(master=CREATE_FRAME, text='Copy output')
COPY_BUTTON.grid(column=0, row=7, sticky=tk.S+tk.W)
COPY_BUTTON.bind("<Button>", handle_copy)

def handle_pack(event):
    # print compact output string which uses less memory, but must be unpacked to be used.
    output = ''

    shape = TOTAL_SHAPE + [CURRENT_ACTION]
    for item in shape:
        if item['coords']:
            
            clr_txt = 'u' if item['color'] == UI_COLOR else 'b'
            
            coords_txt = 'a' + str(item['coords']).replace('[','(').replace(']',')').replace(' ','')

            output += f"{coords_txt}, {clr_txt}, {item['fill']},"
    
    
    output = output.replace(
        ' ',''
    ).replace(
        ',False','f'
    ).replace(
        ',True','t'
    ).replace(
        '),u','u'
    ).replace(
        '),b','b'
    ).replace(
        'a(','a'
    )

    output = PACKED_PREFIX + '"' + output + '"' + '\n\n\n\n' + UNPACK_HINT
    gui_print(output)
    
PACK_BUTTON = tk.Button(master=CREATE_FRAME, text='Pack output')
PACK_BUTTON.grid(column=2, row=7, sticky=tk.S+tk.E)
PACK_BUTTON.bind("<Button>", handle_pack)


OUTPUT_BOX = tk.Text(master=CREATE_FRAME)
OUTPUT_BOX.grid(column=0, row=6, columnspan=3, sticky=STICKY_ALL)




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
            fill="Gray" if y % 4 == 0 else "Lavender"
        )
    for x in range(WIDTH):
        CANVAS.create_line(
            (
                x*PX_SIZE,
                0,
                x*PX_SIZE,
                CANVAS_HEIGHT,
            ),
            fill="Gray" if x % 4 == 0 else "Lavender"
        )

def gui_print(text):
    global output_box
    OUTPUT_BOX.delete("1.0", tk.END)
    OUTPUT_BOX.insert("1.0", text)






def format_print_shape():
    # print readable output str

    output = OUTPUT_PREFIX

    shape = TOTAL_SHAPE + [CURRENT_ACTION]
    for item in shape:
        if item['coords']:
            
            clr_txt = UI_CLR_TEXT if item['color'] == UI_COLOR else BG_CLR_TEXT
            
            coords_txt = COORD_PREFIX + str(item['coords']).replace('[','(').replace(']',')').replace(' ','') + COORD_SUFFIX
            
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


    img = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT))
    img.paste(IMAGE.resize((CANVAS_WIDTH, CANVAS_HEIGHT)))

    if BG_IMAGE:
        bg = BG_IMAGE.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        bg.putalpha(TRACE_ALPHA)
        img.alpha_composite(bg)

    PHOTO_IMG.paste(img)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rule_lines()
CANVAS.bind("<Button>", click_handler)



WINDOW.mainloop()
