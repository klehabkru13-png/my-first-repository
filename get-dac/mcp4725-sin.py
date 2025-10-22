import time
import RPi.GPIO as GPIO
from math import sin, pi
from mcp4725 import MCP4725  

def get_sin_wave_amplitude(freq, t):
    Y = sin(2 * pi * freq * t) + 1
    YY = Y / 2
    return YY

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1.0 / sampling_frequency)

if name == "main":
    mcp = MCP4725(5, 0x61, True)
    signal_amplitude = 2.0  
    signal_frequency = 10.0 
    sampling_frequency = 1000.0  
    
    current_time = 0.0
    
    try:
        while True:
            YY_amp = get_sin_wave_amplitude(signal_frequency, current_time)
            voltage = signal_amplitude * YY_amp
            mcp.set_voltage(voltage)
            wait_for_sampling_period(sampling_frequency)
            current_time += 1.0 / sampling_frequency

    except KeyboardInterrupt:
        print("\nОстановка по Ctrl+C...")
    finally:
        mcp.deinit()