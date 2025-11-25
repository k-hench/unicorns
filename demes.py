import time
import math
import random
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

# set deme boundaries
# xw = int(height)
# demes_min_x = [ 0, 0 ]
# demes_max_x = [ xw, xw ]
xw = int(height/ 4)
demes_min_x = [ 0, 0, xw, xw, 2*xw, 2*xw, 3*xw, 3*xw ]
demes_max_x = [ xw, xw, 2*xw, 2*xw, 3*xw, 3*xw, height, height ]

yh = int(width/ 2)
# demes_min_y = [ 0, yh ]
# demes_max_y = [ yh , width ]
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
    current_color = graphics.create_pen(value_x, int(value_x * 0.25), int(value_x * 0.1))
    _set_pen(current_color)
    # do all the painting
    for x in range( x1 ,x2 ):
        for y in range( y1, y2 ):
            _pixel(x, y)
    picounicorn.update(_graphics)

# set_deme(0, 0)

n_demes = len( demes_min_x )
loop_deme = int(0)
current_deme = int(random.uniform(0, (n_demes-1)))
available_demes = [ x for x in range(n_demes) ]
available_demes.pop(current_deme)
pulse_speed = 4400
t_last_stop = start
print("loop: " + str(loop_deme) + " - deme: " + str(current_deme) + " - loop duration: " + str(round(pulse_speed / 1000, 3))) 

while True:
    # 
    t = (time.ticks_ms()-t_last_stop) / pulse_speed

    if t  > 1:
       current_deme = available_demes[int(random.uniform(0, (n_demes-2)))]
       available_demes = [ x for x in range(n_demes) ]
       available_demes.pop(current_deme)
       pulse_speed = random.uniform(1500, 5000)
       t_last_stop = time.ticks_ms()
       t = 0
       loop_deme += 1
       print("loop: " + str(loop_deme) + " - deme: " + str(current_deme)+ " - loop duration: " + str(round(pulse_speed / 1000, 3)))
       

    set_deme(current_deme, t)
    # And sleep, so we update ~ 60fps
    time.sleep(1.0 / 60)