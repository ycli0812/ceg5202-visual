import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, sensors=6):
        plt.ion()
        self.sensors = sensors
        self.figure, self.axes = plt.subplots(ncols=2, nrows=int(np.ceil(sensors / 2)))
        self.axes = np.ndarray.flatten(self.axes)
        if type(self.axes) is not np.ndarray:
            self.axes = np.array([self.axes])
        self.line = self.axes[0].plot(range(100), range(100))

        self.sensor_data: list = np.zeros((6, 2, 0)).tolist()
        plt.suptitle('Sensor Outputs')
        plt.tight_layout()

    def set_subplot_info(self, sensor: int, n_lines: int = None, title: str = None):
        if sensor >= self.sensors:
            print('Error: sensor index exceed')
            return
        axis = self.axes[sensor]
        if n_lines is not None:
            for line in axis.lines:
                line.remove()
            for i in range(n_lines):
                axis.plot([], [])
            self.sensor_data[sensor] = [[] for i in range(n_lines + 1)]

        if title is not None:
            axis.set_title(title)

    def push_sensor_data(self, sensor: int, t: int, vals: list[int | float]):
        if sensor >= self.sensors:
            print('Error: sensor index exceed')
            return
        if len(vals) != len(self.axes[sensor].get_lines()):
            print('Error: too much or too few values')
            return

        self.sensor_data[sensor][0].append(t)
        self.sensor_data[sensor][0] = self.sensor_data[sensor][0][-100:]
        xdata = self.sensor_data[sensor][0]
        max_y, min_y = 0, 99999
        for il, line in enumerate(self.axes[sensor].get_lines()):
            self.sensor_data[sensor][il + 1].append(vals[il])
            self.sensor_data[sensor][il + 1] = self.sensor_data[sensor][il + 1][-100:]
            ydata = self.sensor_data[sensor][il + 1]

            max_y = max(max_y, max(ydata))
            min_y = min(min_y, min(ydata))

            line.set_xdata(xdata)
            line.set_ydata(ydata)

        self.axes[sensor].set_xlim([min(xdata), max(xdata) + 1])
        self.axes[sensor].set_ylim([min_y * (0.99 if min_y > 0 else 1.01), max_y * (1.01 if max_y > 0 else 0.99)])

    def extend_sensor_data(self, sensor: int, t: list[int], vals: list[list[int | float]]):
        if sensor >= self.sensors:
            print('Error: sensor index exceed')
            return
        if len(vals) == 0 or len(vals[0]) != len(self.axes[sensor].get_lines()):
            print('Error: too much or too few values')
            return
        if len(t) != len(vals):
            print('Invalid data')
            return

        self.sensor_data[sensor][0].extend(t)
        self.sensor_data[sensor][0] = self.sensor_data[sensor][0][-100:]
        xdata = self.sensor_data[sensor][0]
        max_y, min_y = 0, 999999
        vals = np.array(vals).transpose()
        for il, line in enumerate(self.axes[sensor].get_lines()):
            self.sensor_data[sensor][il + 1].extend(vals[il].tolist())
            self.sensor_data[sensor][il + 1] = self.sensor_data[sensor][il + 1][-100:]
            ydata = self.sensor_data[sensor][il + 1]

            max_y = max(max_y, max(ydata))
            min_y = min(min_y, min(ydata))

            line.set_xdata(xdata)
            line.set_ydata(ydata)

        self.axes[sensor].set_xlim([min(xdata), max(xdata) + 1])
        self.axes[sensor].set_ylim([min_y * (0.99 if min_y > 0 else 1.01), max_y * (1.01 if max_y > 0 else 0.99)])

    def refresh(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
