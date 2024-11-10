import operator

import cv2
import matplotlib.pyplot as plt

from base_detector import BaseDetector

class HistDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.title = "Гистограмма"
        self.delta_k = 230

    # Гистограмма
    def detect(self, file):
        # Вычисление гистограммы
        histg = cv2.calcHist([file], [0], None, [256], [0, 256])
        return histg

    def check_against_test(self, ref, tst):
        in_e_h, e_m_h = max(enumerate(ref), key=operator.itemgetter(1))
        t_max_h = tst[in_e_h]
        delta_h = abs(e_m_h - t_max_h)

        return 1 if delta_h < self.delta_k else 0

    def plot_func(self):
        # r, = axis.plot(data, color="green")
        return lambda x: plt.plot(x, color="green")

    def plot_func_on_axis(self, axis):
        # r, = axis.plot(data, color="green")
        return lambda x: axis.plot(x, color="green")

    def plot_on_num_ax(self, data, ax_numbered, ax_numbered_2):
        ax_numbered.set_title(data.title)
        data_to_plot = self.correct_plot_data(data.t[0])
        met_a, = self.plot_func_on_axis(ax_numbered)(data_to_plot)
        a_e, = self.plot_func_on_axis(ax_numbered_2)(data.e[0])

        return met_a, a_e