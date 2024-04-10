# polygon-tool
This is a simple tkinter-based GUI for creating polygon definitions, to be used in code.

I made this while working on MicroHydra. I searched online for a tool that did this, but I was surprised to come up empty-handed. 

All this does, is provide a GUI for drawing polygons with the mouse, and it outputs a list of tuples, which can be passed to micropython's FrameBuffer.polygon method as args. (or, of course, the formatting could be changed slightly to output for any other use that needs a list of polygon coordinates).

This tool requires tkinter and Pillow.
