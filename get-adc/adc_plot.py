import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10,6))
    plt.plot(time, voltage)
    plt.xlabel('Ось t (Время, с)')
    plt.ylabel('Ось U (Напряжение, В)')
    plt.xlim(0, 60)
    plt.ylim(0.5,2.6)
    plt.grid(True)
    plt.title(f'Зависимость напряжения от времени (Макс:{max_voltage:.2f}В)')
    plt.show()

def plot_sampling_period_hist(sampling_periods):
    plt.figure(figsize=(10,6))
    plt.hist(sampling_periods, bins=12, range=(0, 0.6))
    plt.xlabel('Период измерения, с')
    plt.ylabel('Количество измерений')
    plt.xlim(0, 0.6)
    plt.grid(True)
    plt.title('Гистограмма периодов дискретизации')
    plt.show()