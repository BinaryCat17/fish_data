import cv2
import numpy as np
from threading import Thread


def stime(dt):
    return dt.strftime("%Y-%m-%d-%H-%M-%S")


def run_daemon(f, *args):
    t = Thread(target=f, args=args)
    t.daemon = True
    t.start()


class Monitor:
    def __init__(self, width, height, enable=True):
        self.imgs = []
        self.width = width
        self.height = height

    def show(self, idx):
        def do_show(img):
            if idx < len(self.imgs):
                self.imgs[idx] = img
            else:
                self.imgs.append(img)
        return do_show

    def update(self):
        if not self.enable:
            return

        im = np.concatenate(self.imgs, axis=0)
        im = cv2.resize(im, (self.width, self.height))
        cv2.imshow('frames', im)
