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

temp_store = {
    'ACC': {
        'x': [],
        'y': [],
    },
    'PRS': {
        'x': [],
        'y': [],
    },
    'GYR': {
        'x': [],
        'y': [],
    },
    'HUM': {
        'x': [],
        'y': [],
    },
    'MAG': {
        'x': [],
        'y': [],
    },
    'TMP': {
        'x': [],
        'y': [],
    },
    'MLR': {
        'x': [],
        'y': [],
    },
}


def sanitize_text(raw: bytes):
    if raw.endswith(b'\r\n'):
        return raw[:-2].decode('utf8')

    if raw.endswith(b'\n') or raw.endswith(b'\r'):
        return raw[:-1].decode('utf8')


def push_store(name, x, y):
    plotter.push_sensor_data(subplot_id_map[name], x, y)
    # temp_store[name]['x'].append(x)
    # temp_store[name]['y'].append(y)
    # if len(temp_store[name]['x']) >= 10:
    #     plotter.extend_sensor_data(sensor, temp_store[name]['x'], temp_store[name]['y'])
    #     temp_store[name]['x'].clear()
    #     temp_store[name]['y'].clear()


def parse_data(text: str):
    try:
        name, tick, num, *data = text.split(',')
        data = [float(n) for n in data]
        num = int(num)
        tick = int(tick)
        if num != len(data):
            raise Exception('Data package broken')
    except Exception as e:
        return
    if name == 'MLR':
        print(f'Model predict: {motions[int(data[0])]}')
    else:
        plotter.push_sensor_data(subplot_id_map[name], tick, data)
    # match name:
    #     case 'ACC' as name:
    #         push_store(name, tick, data)
    #     case 'PRS' as name:
    #         push_store(name, tick, data)
    #     case 'GYR' as name:
    #         push_store(name, tick, data)
    #     case 'HUM' as name:
    #         push_store(name, tick, data)
    #     case 'TMP' as name:
    #         push_store(name, tick, data)
    #     case 'MAG' as name:
    #         push_store(name, tick, data)
    #     case 'MLR':
    #         print(f'Model predict: {motions[int(data[0])]}')


def main():
    plotter.set_subplot_info(sensor=subplot_id_map['ACC'], n_lines=3, title='Acceleration')
    plotter.set_subplot_info(sensor=subplot_id_map['GYR'], n_lines=3, title='Gyroscope')
    plotter.set_subplot_info(sensor=subplot_id_map['MAG'], n_lines=3, title='Magnitude')
    plotter.set_subplot_info(sensor=subplot_id_map['HUM'], n_lines=1, title='Humidity')
    plotter.set_subplot_info(sensor=subplot_id_map['TMP'], n_lines=1, title='Temperature')
    plotter.set_subplot_info(sensor=subplot_id_map['PRS'], n_lines=1, title='Pressure')

    with serial.Serial(com, 115200, timeout=1) as ser:
        line_counter = 0
        while True:
            line = sanitize_text(ser.readline())
            parse_data(line)
            line_counter += 1
            if line_counter >= 28:
                plotter.refresh()
                line_counter = 0


if __name__ == '__main__':
    main()



