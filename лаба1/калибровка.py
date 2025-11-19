import numpy as np
import matplotlib.pyplot as plt
voltage = [0.606, 1.095, 1.569, 2.033]
pressure = [40, 80, 120, 160]


plt.figure(figsize=(10,6))
plt.plot(pressure, voltage, 'ro-')
plt.xlabel('Ось t (Время, с)')
plt.ylabel('Ось U (Напряжение, В)')
plt.xlim(0, 200)
plt.ylim(0,4)
plt.grid(True)

plt.show()