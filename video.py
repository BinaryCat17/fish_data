import cv2
from queue import Queue
from utils import run_daemon
import numpy as np


class FileVideoStream:
    def __init__(self, path, mode, queueSize=128):
        self.stream = cv2.VideoCapture(path, mode)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        run_daemon(self.update)
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            if not self.Q.full():
                (grabbed, frame) = self.stream.read()
                if not grabbed:
                    self.stop()
                    return
                self.Q.put(frame)

    def is_opened(self):
        return self.stream.isOpened()

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True

    def release(self):
        self.stream.release()


class Video:
    def __init__(self, cam, max_res, fps, mode=cv2.CAP_ANY, show=None):
        self.show = show

        self.cap = FileVideoStream(cam, mode)
        self.cap.stream.set(cv2.CAP_PROP_FRAME_WIDTH, max_res[0])
        self.cap.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, max_res[1])
        self.cap.stream.set(cv2.CAP_PROP_FPS, fps)

        self.width = int(self.cap.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.stream.get(cv2.CAP_PROP_FPS))

        if self.fps == 0:
            self.fps = fps

        print(f'Camera res ({self.width}, {self.height}) FPS {self.fps}')

        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        self.cap.start()

    def pause(self):
        self.out.release()

    def prepare(self, filename):
        self.out = cv2.VideoWriter(
            filename, self.fourcc, self.fps, (self.width, self.height))

    def stop(self):
        cv2.destroyAllWindows()
        self.cap.release()
        self.out.release()

    def capture(self, now):
        if self.cap.is_opened():
            frame = self.cap.read()
            self.out.write(frame)
            if self.show is not None:
                self.show(frame)
            return True
        else:
            print('Can\'t open file')
        return False
