import time
import math
import random
import sys
from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK

picounicorn = PicoUnicorn()
graphics = PicoGraphics(display = DISPLAY_UNICORN_PACK)

@micropython.native  # noqa: F821
def draw(t, deme):
    # take local references as it's quicker than accessing the global
    # and we access it a lot in this method
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel
    
    picounicorn.update(_graphics)

# init conditions
width = picounicorn.get_height()
height = picounicorn.get_width()
start = time.ticks_ms()
pulse_speed = 4400

# set deme boundaries
xw = int(height/ 4)
demes_min_x = [ 0, 0, xw, xw, 2*xw, 2*xw, 3*xw, 3*xw ]
demes_max_x = [ xw, xw, 2*xw, 2*xw, 3*xw, 3*xw, height, height ]

yh = int(width/ 2)
demes_min_y = [ 0, yh, 0, yh, 0, yh, 0, yh ]
demes_max_y = [ yh , width, yh , width, yh , width, yh , width ]

def set_deme(deme_int, t_deme):
    [ x1, x2, y1, y2 ] = [ demes_min_x[deme_int], demes_max_x[deme_int], demes_min_y[deme_int], demes_max_y[deme_int] ]
    # take local references as it's quicker than accessing the global
    # and we access it a lot in this method
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel
    value_x = int(255 * 0.5 * (1 - math.cos(math.pi * 2 * t_deme) ))
    current_color = graphics.create_pen(value_x, int(value_x * 0.5), int(value_x * 0.2))
    _set_pen(current_color)
    # do all the painting
    for x in range( x1 ,x2 ):
        for y in range( y1, y2 ):
            _pixel(x, y)
    picounicorn.update(_graphics)

# set_deme(0, 0)

n_demes = len( demes_min_x )
loop_deme = int(1)
current_deme = int(random.uniform(0, (n_demes-1)))

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"
    #cursor up one line
    sys.stdout.write('\x1b[1A')
    #delete last line
    sys.stdout.write('\x1b[2K')

print("init")

while True:
    t = (time.ticks_ms()-start) / pulse_speed # pulse speed 3600
    #ty = (time.ticks_ms()-start-(pulse_speed*0.5)) / pulse_speed 

    t_intesity = t - int(t)
    delete_last_line()
    print(str(t_intesity) + "", end='')
    print("")

    if t  > (loop_deme + 1):
       current_deme = int(random.uniform(0, (n_demes-1)))
       print(current_deme)
       loop_deme = int(t)
       print(loop_deme)
       print("-----")

    set_deme(current_deme, t_intesity)
    # And sleep, so we update ~ 60fps
    time.sleep(1.0 / 60)