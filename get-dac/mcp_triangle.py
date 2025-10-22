import time
import RPi.GPIO as GPIO
from math import sin, pi
from mcp4725 import MCP4725  

def get_triangle_wave_amplitude(freq, t):
    phase = (freq * t) % 1.0 
    if phase < 0.5:
        value = 4 * phase - 1.0  
    else:
        value = 3.0 - 4 * phase  
    yy = (value + 1.0) / 2.0 
    return yy
def wait_for_sampling_period(sampling_frequency):
    time.sleep(1.0 / sampling_frequency)

if __name__ == "__main__":
    mcp = MCP4725(5, 0x61, True)
    signal_amplitude = 2.0  
    signal_frequency = 10.0 
    sampling_frequency = 1000.0  
    
    current_time = 0.0
    
    try:
        while True:
            YY_amp = get_triangle_wave_amplitude(signal_frequency, current_time)
            voltage = signal_amplitude * YY_amp
            mcp.set_voltage(voltage)
            wait_for_sampling_period(sampling_frequency)
            current_time += 1.0 / sampling_frequency

    except KeyboardInterrupt:
        print("\nОстановка по Ctrl+C...")
    finally:
        mcp.deinit()