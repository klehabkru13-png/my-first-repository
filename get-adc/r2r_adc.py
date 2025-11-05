import time
import RPi.GPIO as GPIO

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    
    def dec2bin(self, number):
        return [int(element) for element in bin(number)[2:].zfill(8)]
    
    def number_to_dac(self, number):
        num = self.dec2bin(number)
        if self.verbose:
            print(number, num)
        for i, pin in enumerate(self.bits_gpio):
            GPIO.output(pin, num[i])
    
    def sequential_counting_adc(self):
        value = 0
        while value < 256:
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            comp = GPIO.input(self.comp_gpio)
            if comp == 1:
                return max(0, value-1)
            value += 1
        if comp == 0:
            return 255
    
    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        return digital_value * self.dynamic_range / 255
    
    def successive_approximation_adc(self):
        low = 0
        high = 255
        result = 0
        
        for _ in range(8):
            mid = (low + high) // 2
            self.number_to_dac(mid)
            time.sleep(self.compare_time)
            
            comp = GPIO.input(self.comp_gpio)
            
            if comp == 1:
                high = mid - 1 
                result = mid
            else:
                low = mid + 1
        
        return result
    
    def get_sar_voltage(self):
        digital_value = self.successive_approximation_adc()
        return digital_value * self.dynamic_range / 255

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.201, 0.01, True)
        
        while True:
            try:
                #voltage_sc = adc.get_sc_voltage()
                voltage_sar = adc.get_sar_voltage()
                
                print(f"Successive: {voltage_sar:.3f}V")

            except ValueError:
                print("Ошибка значения")
            except KeyboardInterrupt:  
                print("Прервано пользователем")
                break

    finally:
        adc.deinit()