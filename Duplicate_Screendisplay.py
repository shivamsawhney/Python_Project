import pyglet
window = pyglet.window.Window()
context = window.context
config = context.config
config.double_buffer
c_int(1)
config.stereo
c_int(0)
config.sample_buffers
c_int(0)

platform = pyglet.window.get_platform()
display = platform.get_default_display()
display = platform.get_display('remote:1.0')
display = platform.get_display(':0.1')

for screen in display.get_screens():   \\to print screen on another screen

XlibScreen(screen=0, x=1280, y=0, width=1280, height=1024, xinerama=1)
XlibScreen(screen=0, x=0, y=0, width=1280, height=1024, xinerama=1)