import time
import math
import random
from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK

picounicorn = PicoUnicorn()
graphics = PicoGraphics(display=DISPLAY_UNICORN_PACK)

@micropython.native  # noqa: F821
def draw(t,vx,vy,dc):
    # take local references as it's quicker than accessing the global
    # and we access it a lot in this method
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel

    for y in range(picounicorn.get_height()):
        for x in range(picounicorn.get_width()):
          if x == vy:
            value_x = int(255 * 0.5 * (1 - math.cos(math.pi * 2 * t) ))
            current_color = graphics.create_pen(value_x, value_x, value_x)
            _set_pen(current_color)
            _pixel(x, y)
          if t > 0.5:
            if y == vx:
              y_dim =   0.5 * (1 + math.cos(math.pi * 2 * t) )
              value_y = int(255 * y_dim)
              value_ry = int(125 * y_dim + 130) 
              if x == vy:
                current_color = dc
              else:
                current_color = graphics.create_pen(value_y, value_y, value_y)
              _set_pen(current_color)
              _pixel(x, y)

    picounicorn.update(_graphics)

# init conditions
width = picounicorn.get_height()
height = picounicorn.get_width()
start = time.ticks_ms()
x_loop = int(1)
y_loop = int(1)
vx = 3
vy = 7
pulse_speed = 4400

dot_colours = [graphics.create_pen(255, 0, 0),
               graphics.create_pen(155, 85, 0),
               graphics.create_pen(120, 0, 120),
               graphics.create_pen(0, 130, 0),
               graphics.create_pen(0,0, 140)]
current_dot = dot_colours[3]

while True:
    t = (time.ticks_ms()-start) / pulse_speed # pulse speed 3600
    ty = (time.ticks_ms()-start-(pulse_speed*0.5)) / pulse_speed 

    if t  > (x_loop + 1):
       vy = int(random.uniform(1, height))
       x_loop = int(t)
    if ty > (y_loop + 1):
       vx = int(random.uniform(1, width))
       current_dot = dot_colours[int(random.uniform(0, 4))]
       y_loop = int(t)

    draw(t, vx, vy, current_dot)

    # And sleep, so we update ~ 60fps
    time.sleep(1.0 / 60)