#!/usr/bin/env python

# measuring heartbeat and have lightshow corresponding to it

# using: MAX30105 breakout to measure heartrate and 5x5 RGB as display for lightshow
# using code fragments from Pimoroni https://github.com/pimoroni https://github.com/pimoroni/breakout-garden
# https://github.com/pimoroni/rgbmatrix5x5-python/blob/master/examples/blinkyspot.py

import colorsys
import time

try:
    import numpy
except ImportError:
    exit('This script requires the numpy module\nInstall with: sudo pip install numpy')
    
from threading import Thread
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

from rgbmatrix5x5 import RGBMatrix5x5

from max30105 import MAX30105, HeartRate


# Set up MAX30105 Breakout
max30105 = MAX30105()
max30105.setup(leds_enable=2)

max30105.set_led_pulse_amplitude(1, 0.2)
max30105.set_led_pulse_amplitude(2, 12.5)
max30105.set_led_pulse_amplitude(3, 0)

max30105.set_slot_mode(1, 'red')
max30105.set_slot_mode(2, 'ir')
max30105.set_slot_mode(3, 'off')
max30105.set_slot_mode(4, 'off')

hr = HeartRate(max30105)
data = []
running = True

bpm = 0
bpm_avg = 0
beat_detected = False
beat_status = False

rgbmatrix5x5 = RGBMatrix5x5()

rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.8)

height = rgbmatrix5x5.height
width = rgbmatrix5x5.width

rgbmatrix5x5.clear()
rgbmatrix5x5.show()

if 1 == 1:
    average_over = 5
    bpm_vals = [0 for x in range(average_over)]
    last_beat = time.time()

    while running:
        t = time.time()
        samples = max30105.get_samples()
        if samples is not None:
            for i in range(0, len(samples), 2):
                ir = samples[i + 1]
                beat_detected = hr.check_for_beat(ir)
                if beat_detected:
                    print("beep")
                    rand_mat = numpy.random.rand(width, height)
                    for y in range(height):
                        for x in range(width):
                            h = 0.1 * rand_mat[x, y]
                            s = 0.8
                            v = rand_mat[x, y]
                            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]
                            rgbmatrix5x5.set_pixel(x, y, r, g, b)
                    rgbmatrix5x5.show()
                    rgbmatrix5x5.clear()
                    time.sleep(0.05)
                    rgbmatrix5x5.show()

