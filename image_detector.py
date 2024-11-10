import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

from base_detector import BaseDetector
from method_data import MethodData
from plot_data import PlotData


class ImageDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.title = "Изображение"
        self.ax = None
        self.ax_ind = None
        self.ax_numbered = None
        self.ax_numbered_2 = None

    def detect(self, file):
        return file

    def correct_plot_data(self, raw_data):
        return raw_data

    def detect_from_file(self, path):
        e_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return self.detect(e_img)

    def check_against_test(self, ref, tst):
        return 1

    def build_chart(self,
                    num_e,
                    num_c,
                    start_pos,
                    step,
                    end_pos,
                    ch_func):
        t_det = []
        e_det = []

        if ch_func == 0:
            help_pos = num_e
        if ch_func == 1:
            help_pos = 1
        if ch_func == 2:
            help_pos = 0

        num_subfolders = len([f.path for f in os.scandir("Test1") if f.is_dir()])

        for i in range(1, num_subfolders+1, 1):
            num_files = len(
                [
                    f for f in os.listdir(f"Test1/s{i}") if os.path.isfile(
                        os.path.join(f"Test1/s{i}", f)
                    )
                ]
            )

            # Перебор эталонов
            for j in range(start_pos, end_pos + 1, step):
                e_det.append(
                    self.detect_from_file(f"Test1/s{i}/{j}.jpg")
                )

                #перебор тестов
                for k in range(help_pos + 1, num_files + 1, step):
                    t_det.append(
                        self.detect_from_file(f"Test1/s{i}/{k}.jpg")
                    )

        return MethodData(self.title,[], [], t_det, e_det, [])


    def plot_func(self):
        return lambda x: plt.imshow(x, cmap='gray')

    def plot_func_on_axis(self, axis):
        return lambda x: axis.imshow(x, cmap='gray')

    def plot_on_num_ax(self, data, ax_numbered, ax_numbered_2):
        data_to_plot_1 = self.correct_plot_data(data.t[0])
        met_a = self.plot_func_on_axis(ax_numbered)(data_to_plot_1)

        ax_numbered_2.set_title(data.title)
        data_to_plot_2 = self.correct_plot_data(data.e[0])
        a_e = self.plot_func_on_axis(ax_numbered_2)(data_to_plot_2)

        return met_a, a_e

    def init_plot(self, data, ax, ax_ind, ax_numbered, ax_numbered_2):
        self.ax_numbered = ax_numbered
        self.ax_numbered_2 = ax_numbered_2

        met_a, a_e = self.plot_on_num_ax(data, ax_numbered, ax_numbered_2)

        return PlotData(met_a, a_e, None, None)

    def plot_stat(self, data, plot_data, current_index):
        assert False

    def update_numbered_axis(self, data, index):
        assert False

    def show_mean(self, plot_data, data, put):
        assert False
