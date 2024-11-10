import cv2
import numpy as np
from matplotlib import pyplot as plt

from base_detector import BaseDetector

class DctDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.title = "DCT"

    def detect(self, file):
        dct = cv2.dct(np.float32(file))
        return dct

    def check_against_test(self, ref, tst):
        # вычисление среднего по эталону, dct
        linalg_norm_e = np.linalg.norm(ref)
        # вычисление среднего по тестовому, dct
        linalg_norm_t = np.linalg.norm(tst)
        # вычисление процента совпадения
        similarity_percent_dct = linalg_norm_t / linalg_norm_e
        if similarity_percent_dct > 1:
            similarity_percent_dct = 2 - similarity_percent_dct
        return similarity_percent_dct

    def correct_plot_data(self, raw_data):
        return np.abs(np.round(raw_data, decimals=3))

    def plot_func(self):
        return lambda x: plt.imshow(x, vmin=0, vmax=255)

    def plot_func_on_axis(self, axis):
        return lambda x: axis.imshow(x, vmin=0, vmax=255)
