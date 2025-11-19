import smbus
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose
    def deinit(self):
        self.bus.close()
    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")
        return number
    def get_voltage(self):
        get_voltage = self.get_number()*self.dynamic_range/644
        return get_voltage

if __name__ == "__main__":
    mcp = None
    try:
        mcp = MCP3021(3.278, True)
        
        while True:
            try:
                voltage = mcp.get_voltage()
                print(f"{voltage:.3f}V")
                time.sleep(1)

            except KeyboardInterrupt:
                print("\nВыход по Ctrl+C")
            except Exception as e:
                print(f"Ошибка: {e}")
    finally:
        if mcp:
            mcp.deinit()