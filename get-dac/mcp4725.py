import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)
        
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")

        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
                print("Устанавливаем 0.0 В")
            number = 0
        else:
            number = int(4095 * voltage / self.dynamic_range)  
        self.set_number(number)
        
        if self.verbose:
            print(f"Установлено напряжение: {voltage:.2f} В (число: {number}/4095)\n")

if __name__ == "__main__":
    mcp = None
    try:
        mcp = MCP4725(5, 0x61, True)
        
        while True:
            try:
                user_input = input("Введите напряжение в Вольтах (или 'q' для выхода): ")
                if user_input.lower() == 'q':
                    break
                voltage = float(user_input)
                mcp.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
            except KeyboardInterrupt:
                print("\nВыход по Ctrl+C")
                break

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if mcp:
            mcp.deinit()
