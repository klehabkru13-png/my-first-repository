import time
import RPi.GPIO as GPIO
import adc_plot
from mcp3021_driver import MCP3021
def round_to_step(value, step=0.05, max_value=0.6):
    rounded = round(value / step) * step
    return min(max(rounded, 0), max_value) 
if __name__ == "__main__":
    mcp = MCP3021(5, True) 
    voltage_values = []
    time_values = []
    sampling_periods = []
    duration = 60.0
    start_time = time.time()
        
    try:
        while (time.time()-start_time)< duration:
            voltage = mcp.get_voltage()
            voltage_values.append(voltage)
            time_values.append(time.time()-start_time)
            max_voltage = max(voltage_values)
        sampling_periods = [round_to_step(time_values[i] - time_values[i-1]) 
            for i in range(1, len(time_values))]
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, max_voltage)
        adc_plot.plot_sampling_period_hist(sampling_periods)
        voltage__values = voltage_values[24::25]
        time__values = time_values[24::25]
        voltage___values = [round(x,5) for x in voltage__values]
        time___values = [round(x,4) for x in time__values]
        print(voltage___values)
        print(time___values)
    except ValueError:
        print()

    finally:
        mcp.deinit()    

