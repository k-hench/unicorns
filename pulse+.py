import time
import math
from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK

picounicorn = PicoUnicorn()
graphics = PicoGraphics(display=DISPLAY_UNICORN_PACK)

@micropython.native  # noqa: F821
def draw(t):
    # take local references as it's quicker than accessing the global
    # and we access it a lot in this method
    _graphics = graphics
    _set_pen = graphics.set_pen
    _pixel = graphics.pixel

    for y in range(picounicorn.get_height()):
        for x in range(picounicorn.get_width()):
          if x == 7:
            value_x = int(255 * 0.5 * (1 - math.cos(math.pi * 2 * t) ))
            current_color = graphics.create_pen(value_x, value_x, value_x)
            _set_pen(current_color)
            _pixel(x, y)
          if t > 0.5:
            if y == 3:
              y_dim =   0.5 * (1 + math.cos(math.pi * 2 * t) )
              value_y = int(255 * y_dim)
              if x == 7:
                current_color = graphics.create_pen(255, 0, 0)
              else:
                current_color = graphics.create_pen(value_y, value_y, value_y)
              _set_pen(current_color)
              _pixel(x, y)

    picounicorn.update(_graphics)

start = time.ticks_ms()

while True:
    t = (time.ticks_ms()-start) / 5400 # pulse speed 3600
    draw(t)
    # And sleep, so we update ~ 60fps
    time.sleep(1.0 / 60)