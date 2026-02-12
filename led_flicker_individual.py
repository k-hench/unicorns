from machine import Pin, PWM
import time
import math
import random
import ease

start = time.ticks_ms()

# Step size for changing the duty cycle
duty_step = 129
# Set PWM frequency
frequency = 5000

# init pins
leds_pin = [ Pin(x) for x in range(9, 14) ]
leds_pmw = [ PWM(x) for x in leds_pin ]
[ x.freq(frequency) for x in leds_pmw ]

n_leds = len(leds_pmw)

# initial values per led
pulse_speeds = [ 3000 ] * n_leds
t_last_stops = [ start ] * n_leds

def flicker_sin(t):
  return(0.15 * ( 0.5 * (1 - math.cos(math.pi * 2 * t) ) ))

flickers = [ease.mapping_1, ease.mapping_2, ease.mapping_3, ease.mapping_4, ease.mapping_5 ] + [ flicker_sin ] * 10
n_flickers = len(flickers)
current_flickers = [ flickers[int(random.uniform(0, n_flickers - 1))] for _ in range(n_flickers) ]

def scl(x):
  return(int(35536 * x))

def set_led_brightness(idx, light):
  leds_pmw[idx].duty_u16(scl(light))

loops = [0] * n_leds

while True:
  ts = [ (time.ticks_ms() - t_last_stops[idx]) / pulse_speeds[idx] for idx in range(n_leds) ]

  
  for current_led in range(n_leds):
    if ts[current_led]  > 1:
       # sample new flicker pattern
       current_flickers[current_led] = flickers[int(random.uniform(0, n_flickers - 1))]
       # set new pulse speed
       pulse_speeds[current_led] = random.uniform(4000, 10000)
       # reset timers
       t_last_stops[current_led] = time.ticks_ms()
       loops[current_led] += 1
       print("led_" + str(current_led) + "\tflicker: " + str(current_led)+ "\tloop " + str(loops[current_led]) + "\tduration: " + str(round(pulse_speeds[current_led]  / 1000, 3)))
       ts[current_led] = 0

 
    # set led brightness 
    set_led_brightness(current_led, current_flickers[current_led](ts[current_led]))
      
  time.sleep(1/24)