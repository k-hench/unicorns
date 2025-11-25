import time
import math
import random
from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK

picounicorn = PicoUnicorn()
graphics = PicoGraphics(display = DISPLAY_UNICORN_PACK)

@micropython.native  # noqa: F821
def draw(t, deme, clr_int):
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
demes_min_y = [ 0, yh + 1, 0, yh + 1, 0, yh + 1, 0, yh + 1 ]
demes_max_y = [ yh , width, yh , width, yh , width, yh , width ]

def set_deme(deme_int, t_deme, clr):
    [ x1, x2, y1, y2 ] = [ demes_min_x[deme_int], demes_max_x[deme_int], demes_min_y[deme_int], demes_max_y[deme_int] ]
    # take local references as it's quicker than accessing the global
    # and we access it a lot in this method
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel
    _create_pen = graphics.create_pen
    
    # value_x = int(255 * 0.5 * (1 - math.cos(math.pi * 2 * t_deme) ))
    value_x = 0.5 * (1 - math.cos(math.pi * 2 * t_deme) )
    # do all the painting
    for y in range( y1, y2 ):
        if (y == 0) or (y == (width-1)):
            current_color = _create_pen( int(100 * value_x),
                                         int(100 * value_x),
                                         int(100 * value_x))
            _set_pen(current_color)
        else:
            current_color = _create_pen( int(clr[0] * value_x),
                                         int(clr[1] * value_x),
                                         int(clr[2] * value_x))
            _set_pen(current_color)
        for x in range( x1 , x2 ):
            _pixel(x, y)
    
    x_prog = int(height * t_deme)
    x_prog_intensity = (height * t_deme) - x_prog
    x_prog_clr = int(75 * x_prog_intensity)
    current_color_x = graphics.create_pen(x_prog_clr, x_prog_clr, x_prog_clr)
    _set_pen(current_color_x)
    if (loop_deme % 2) == 0:
        x_id = x_prog
    else:
        x_id = height - x_prog
    _pixel(x_id, yh)
    
    picounicorn.update(_graphics)

def clear_progress():
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel
    _create_pen = graphics.create_pen
    for x_prog in range( height ):
        current_color_x = _create_pen(0,0,0)
        _set_pen(current_color_x)
        _pixel(x_prog, yh)
    
    picounicorn.update(_graphics)

n_demes = len( demes_min_x )
loop_deme = int(0)
current_deme = int(random.uniform(0, (n_demes-1)))
available_demes = [ x for x in range(n_demes) ]
available_demes.pop(current_deme)
pulse_speed = 4400
t_last_stop = start

print("loop: " + str(loop_deme) + " - deme: " + str(current_deme) + " - loop duration: " + str(round(pulse_speed / 1000, 3))) 


clr_x = [[ 255, 0, 0 ], [ 155, 85, 0 ], [ 120, 0, 120 ], [ 0, 130, 0 ], [ 0, 0, 140 ]]
clr = clr_x[int(random.uniform(0, 4))]

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
       clr = clr_x[int(random.uniform(0, 4))]
       clear_progress()
       print("loop: " + str(loop_deme) + " - deme: " + str(current_deme)+ " - loop duration: " + str(round(pulse_speed / 1000, 3)))
       

    set_deme(current_deme, t, clr)
    # And sleep, so we update ~ 60fps
    time.sleep(1.0 / 60)