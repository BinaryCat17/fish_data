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
    def __init__(self, width, height):
        self.imgs = []
        self.width = width
        self.height = height

    def show(self, idx, img):
        if idx < len(self.imgs):
            self.imgs[idx] = img
        else:
            self.imgs.append(img)

    def update(self):
        im = np.concatenate(self.imgs, axis=0)
        im = cv2.resize(im, (self.width, self.height))
        cv2.imshow('frames', im)
