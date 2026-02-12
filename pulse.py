from machine import Pin, PWM
import time
import math

start = time.ticks_ms()
pulse_speed = 500
duty_step = 129  # Step size for changing the duty cycle
#Set PWM frequency
frequency = 5000


[ led_09, led_10, led_11, led_12, led_13 ] = [ Pin(9), Pin(10), Pin(11), Pin(12), Pin(13) ]
[ led_pwm_09 , led_pwm_10 , led_pwm_11 , led_pwm_12 , led_pwm_13 ] = [ PWM(led_09), PWM(led_10), PWM(led_11), PWM(led_12), PWM(led_13) ]
leds_pmw = [ led_pwm_09 , led_pwm_10 , led_pwm_11 , led_pwm_12 , led_pwm_13 ]
[ x.freq(frequency) for x in leds_pmw ]
led_order = [ 0, 1, 2, 3, 4, 3, 2, 1 ]

def scl(x):
  return(int(35536 * x))

def set_led_brightness(idx, light):
  leds_pmw[idx].duty_u16(scl(light))

[ x for x in range(5) ]

while True:
  t = (time.ticks_ms()-start) / pulse_speed 
  lightness = 0.5 * (1 - math.cos(math.pi * 2 * t) )
  [ set_led_brightness(x, lightness) for x in range(5) ]
  # print(led_order[int(t) % len(led_order)])
  time.sleep(1/24)