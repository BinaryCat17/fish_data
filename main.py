import datetime
import cv2
from utils import stime
from serializer import Serializer
from video import Video
from water_sensor import WaterSensor
from utils import run_daemon
from utils import Monitor


class App:
    def __init__(self, seconds):
        self.seconds = seconds
        self.backup_time = datetime.datetime.now()
        self.sensors = []
        self.updaters = []

    def add_sensor(self, sensor, folder, format):
        self.sensors.append((sensor, folder, format))

    def add_updater(self, updater):
        self.updaters.append(updater)
        
    def run(self):
        print('Init...')
        for sensor, folder, format in self.sensors:
            sensor.prepare(
                f'data/{folder}/out-{stime(self.backup_time)}._{format}')

        while 1:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            now = datetime.datetime.now()
            for s in self.sensors:
                s[0].capture(now)

            for u in self.updaters:
                u.update()

            if (now - self.backup_time).total_seconds() > self.seconds:
                self._backup(now)

        self._backup(datetime.datetime.now())

    def _backup(self, now):
        print(f'Backup ({stime(self.backup_time)}) ...', end=" ")

        for s in self.sensors:
            s[0].pause()

        for sensor, folder, format in self.sensors:
            run_daemon(
                serializer.save,
                f'data/{folder}/out-{stime(self.backup_time)}._{format}')

        self.backup_time = now

        for sensor, folder, format in self.sensors:
            sensor.prepare(
                f'data/{folder}/out-{stime(self.backup_time)}._{format}')

        print('done!')


if __name__ == '__main__':
    serializer = Serializer()
    app = App(30)

    monitor = Monitor(480, 540, False)
    app.add_updater(monitor)

    # app.add_sensor(WaterSensor('COM5'), 'water', 'txt')

    app.add_sensor(
        Video(1, (1920, 1080), 30, cv2.CAP_DSHOW,
              show=monitor.show(0)),
        'webcam', 'mp4')

    app.add_sensor(
        Video('rtsp://admin:@192.168.88.10/1', (1920, 1080), 20,
              show=monitor.show(1)),
        'ip_cam', 'mp4')

    app.run()
