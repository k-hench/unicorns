from machine import Pin, PWM
import time
import math
import random
import ease

start = time.ticks_ms()
pulse_speed = 1500
duty_step = 129 # Step size for changing the duty cycle
#Set PWM frequency
frequency = 5000

loop_led = int(0)
t_last_stop = start

[ led_09, led_10, led_11, led_12, led_13 ] = [ Pin(9), Pin(10), Pin(11), Pin(12), Pin(13) ]
[ led_pwm_09 , led_pwm_10 , led_pwm_11 , led_pwm_12 , led_pwm_13 ] = [ PWM(led_09), PWM(led_10), PWM(led_11), PWM(led_12), PWM(led_13) ]
leds_pmw = [ led_pwm_09 , led_pwm_10 , led_pwm_11 , led_pwm_12 , led_pwm_13 ]
[ x.freq(frequency) for x in leds_pmw ]
# led_order = [ 0, 1, 2, 3, 4, 3, 2, 1 ]

n_leds = len(leds_pmw)
current_led = int(random.uniform(0, n_leds - 1))
available_leds = [ x for x in range(n_leds) ]
available_leds.pop(current_led)

flickers = [ease.mapping_1, ease.mapping_2, ease.mapping_3, ease.mapping_4, ease.mapping_5 ]
n_flickers = len(flickers)
current_flicker = flickers[int(random.uniform(0, n_flickers - 1))]

def scl(x):
  return(int(35536 * x))

def set_led_brightness(idx, light):
  leds_pmw[idx].duty_u16(scl(light))

def dim_leds(leddim, dim):
  [ set_led_brightness(x, dim) for x in leddim ]

while True:
  t = (time.ticks_ms()-t_last_stop) / pulse_speed
  
  if t  > 1:
     flicker_idx = int(random.uniform(0, n_flickers - 1))
     current_flicker = flickers[flicker_idx]
     current_led = available_leds[int(random.uniform(0, (n_leds-1)))]
     available_leds = [ x for x in range(n_leds) ]
     available_leds.pop(current_led)
     pulse_speed = random.uniform(1500, 5000)
     t_last_stop = time.ticks_ms()
     t = 0
     loop_led += 1
     # clr = clr_x[int(random.uniform(0, 4))]
     print(" loop: " + str(loop_led) + " - deme: " + str(current_led)+ " - loop duration: " + str(round(pulse_speed / 1000, 3)))
  
  lightness = current_flicker(t)
  set_led_brightness(current_led, lightness)
  lightness_bg = 0.075 * (1 - math.cos(math.pi * 2 * t) )
  dim_leds(available_leds, lightness_bg)
  # print(led_order[int(t) % len(led_order)])
  time.sleep(1/24)