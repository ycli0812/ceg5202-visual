import numpy as np
import serial
from plot import Plotter

motions = ['stationary', 'walking', 'running']

com = 'COM9'

plotter = Plotter(6)

subplot_id_map = {
    'ACC': 0,
    'PRS': 5,
    'GYR': 1,
    'HUM': 3,
    'MAG': 2,
    'TMP': 4,
    'MLR': None,
}


def sanitize_text(raw: bytes):
    if raw.endswith(b'\r\n'):
        return raw[:-2].decode('utf8')

    if raw.endswith(b'\n') or raw.endswith(b'\r'):
        return raw[:-1].decode('utf8')


def push_store(name, x, y):
    plotter.push_sensor_data(subplot_id_map[name], x, y)


def parse_data(text: str):
    name, tick, num, *data = text.split(',')
    data = [float(n) for n in data]
    num = int(num)
    tick = int(tick)
    if num != len(data):
        raise Exception('Data package broken')

    if name == 'MLR':
        print(f'[{tick}] Prediction: {motions[int(data[0])]}')
    else:
        plotter.push_sensor_data(subplot_id_map[name], tick, data)

    return name, tick, num, data


def main():
    with serial.Serial(com, 115200, timeout=1) as ser:
        plotter.set_subplot_info(sensor=subplot_id_map['ACC'], n_lines=3, title='Acceleration')
        plotter.set_subplot_info(sensor=subplot_id_map['GYR'], n_lines=3, title='Gyroscope')
        plotter.set_subplot_info(sensor=subplot_id_map['MAG'], n_lines=3, title='Magnitude')
        plotter.set_subplot_info(sensor=subplot_id_map['HUM'], n_lines=1, title='Humidity')
        plotter.set_subplot_info(sensor=subplot_id_map['TMP'], n_lines=1, title='Temperature')
        plotter.set_subplot_info(sensor=subplot_id_map['PRS'], n_lines=1, title='Pressure')

        line_counter = 0
        start_tick = None
        data_count = {}
        while start_tick is None or tick - start_tick <= 40 * 1000:
            line = sanitize_text(ser.readline())
            try:
                name, tick, num, data = parse_data(line)
                if start_tick is None:
                    start_tick = tick
                if name not in data_count:
                    data_count[name] = 0
                data_count[name] += 1
            except:
                print('Data parse error:', line)

            line_counter += 1
            if line_counter >= 35:
                plotter.refresh()
                line_counter = 0
        print(data_count)


if __name__ == '__main__':
    main()
