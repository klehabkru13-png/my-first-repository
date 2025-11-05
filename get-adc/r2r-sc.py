import time
import RPi.GPIO as GPIO
import adc_plot
from r2r_adc import R2R_ADC
def round_to_step(value, step=0.05, max_value=0.6):
    rounded = round(value / step) * step
    return min(max(rounded, 0), max_value) 
if __name__ == "__main__":
    adc = R2R_ADC(3.201, 0.01, True)
    voltage_values = []
    time_values = []
    sampling_periods = []
    duration = 30.0
    start_time = time.time()
        
    try:
        while (time.time()-start_time)< duration:
            voltage = adc.get_sc_voltage()
            voltage_values.append(voltage)
            time_values.append(time.time()-start_time)
            max_voltage = max(voltage_values)
        sampling_periods = [round_to_step(time_values[i] - time_values[i-1]) 
            for i in range(1, len(time_values))]
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, max_voltage)
        adc_plot.plot_sampling_period_hist(sampling_periods)

    except ValueError:
        print()

    finally:
        adc.deinit()    