import time
from math import pi, sin 
import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, signal_frequency, sampling_frequency, amplitude, verbose = False):
        self.gpio_bits = gpio_bits
        self.signal_frequency = signal_frequency
        self.sampling_frequency = sampling_frequency
        self.amplitude = amplitude
        self.time = 0.0
        self.YY = -amplitude  
        self.step = 4 * signal_frequency * amplitude / sampling_frequency  
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
        
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        
    def dec2bin(self, value):
        return [int(element) for element in bin(value)[2:].zfill(8)]
        
    def set_number(self, Y):
        num = self.dec2bin(Y)
        if self.verbose:
            print(Y, num)
        for i, pin in enumerate(self.gpio_bits):
            GPIO.output(pin, num[i])
            
    def get_triangle_amplitude(self):
        phase = (self.signal_frequency * self.time) % 1
        if phase <= 0.5:
            self.YY += self.step
        else:
            self.YY -= self.step
        Y = int(((self.YY / self.amplitude) + 1) / 2 * 255)
        self.set_number(Y)
        self.time += 1.0 / self.sampling_frequency
        time.sleep(1 / self.sampling_frequency)

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 10, 1000, 3.159, True)
        
        while True:
            dac.get_triangle_amplitude()

    finally:
        dac.deinit()