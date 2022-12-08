import serial
import struct
from utils import stime


class WaterSensor:
    def __init__(self, port):
        self.serialPort = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=8,
            timeout=2,
            stopbits=serial.STOPBITS_ONE)

        self.f_input = open('input.txt', 'ab+')

    def pause(self):
        self.f_output.close()

    def prepare(self, filename):
        self.f_output = open(filename, 'w')

    def stop(self):
        self.f_input.close()
        self.f_output.close()

    def capture(self, now):
        if self.serialPort.in_waiting == 0:
            return

        b = self.serialPort.read_until(b'\xff')

        if len(b) == 11:
            print(
                b, b[1], b[2], b[3], b[4], b[5], b[6],
                struct.unpack('h', b[1:3])[0], struct.unpack('h', b[2:4])[0],
                struct.unpack('h', b[3:5])[0], struct.unpack('h', b[4:6])[0],
                struct.unpack('h', b[5:7])[0]
            )

            Val = self._convert(b[1])
            Val += self._convert(b[2]) / 100.0

            Tf = self._convert(b[4] & 0b00001111)
            Tn = self._convert(b[4] & 0b11110000)
            Td = self._convert(b[3])
            Temp = Td * 10.0 + Tn / 10.0 + Tf / 10.0

            mode = b[5]
            mode_str = 'None'
            if mode == 20:
                mode_str = 'O2'
                Val *= 10.0

            elif mode == 18:
                mode_str = 'DO'

            elif mode == 13:
                mode_str = 'PH'

            elif mode == 49:
                mode_str = 'ORP'

            elif mode == 1:
                mode_str = 'Cond'

            elif mode == 5:
                mode_str = 'TDS'

            elif mode == 9:
                mode_str = "Salt"

            elif mode == 2:
                mode_str = 'Wait'

            print(f'T: {Temp}, {mode_str}: {Val}' + '{0:08b}'.format(b[4]))
            print(f'{stime(now)}, {Temp}, {mode_str}, {Val}',
                  file=self.f_output)

        else:
            print('UNRECOGNIZED:', b)

        self.f_input.write(b)

    def _convert(v):
        return float(hex(v)[2:])
