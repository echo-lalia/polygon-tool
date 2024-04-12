# polygon-tool
This is a simple tkinter-based GUI for creating polygon definitions, to be used in code.

![Screenshot from 2024-04-11 14-54-07](https://github.com/echo-lalia/polygon-tool/assets/108598670/8df0ca58-2e7c-4177-acc0-94ac4ce3e071)



I made this while working on MicroHydra. I searched online for a tool that did this, but I was surprised to come up empty-handed. 

All this does, is provide a GUI for drawing polygons with the mouse, and it outputs a list of tuples, which can be passed to micropython's FrameBuffer.polygon method as args. (or, of course, the formatting could be changed slightly to output for any other use that needs a list of polygon coordinates).

The GUI includes a few simple config options, but there are more options at the top of the script, which you should take a look at if the defaults arent good for you :)

### Usage:
Install Python3, Pillow, and Tkinter. if they arent already.   
Run the script!

This tool also includes a function to "pack" a shape definition into a condensed string to further save memory. 
The string can be 'unpacked' by the program when needed, and converted into an object using string replacement, and the 'exec' command. (an example unpack function is provided with the output when you pack your shape).

In case you're curious, the packed strings use significantly less memory than a bitmap of the icon, from my testing. 
It would also absolutely be possible to 'compress' the strings further and use even less memory, however, I tried keeping it simple to prevent the unpack operation from being too slow. 
