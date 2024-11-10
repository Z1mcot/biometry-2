import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

from method_data import MethodData, SelectedFileData
from plot_data import PlotData


class BaseDetector:
    def __init__(self):
        self.title = None
        self.ax = None
        self.ax_ind = None
        self.ax_numbered = None
        self.ax_numbered_2 = None

    def detect(self, file):
        raise NotImplementedError

    def correct_plot_data(self, raw_data):
        return raw_data

    def detect_from_file(self, path):
        e_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return self.detect(e_img)

    def detect_from_selected_file(self, path):
        return self.detect_from_file(path)

    def check_against_test(self, ref, tst):
        raise NotImplementedError

    # def create_chart_data(self,
    #                 num_e,
    #                 num_c,
    #                 start_pos,
    #                 step,
    #                 end_pos,
    #                 ch_func):
    #     stat_det = []
    #     stat_det_indv = []
    #     t_det = []
    #     e_det = []
    #
    #     ind_et = 0
    #     ind_t = 0
    #
    #     if ch_func == 0:
    #         help_pos = num_e
    #     if ch_func == 1:
    #         help_pos = 1
    #     if ch_func == 2:
    #         help_pos = 0
    #
    #     num_subfolders = num_c
    #
    #     if num_subfolders == 0:
    #         raise Exception("Missing ORLDatabase")
    #
    #     dif = 1
    #
    #     for i in range(1, num_subfolders+1, 1):
    #         sum_det = 0
    #
    #         num_files = len(
    #             [
    #                 f for f in os.listdir(f"ORLdataset/s{i}") if os.path.isfile(
    #                     os.path.join(f"ORLdataset/s{i}", f)
    #                 )
    #             ]
    #         )
    #
    #         # Перебор эталонов
    #         for j in range(start_pos, end_pos + 1, step):
    #             e_det.append(
    #                 self.detect_from_file(f"ORLdataset/s{i}/{j}.pgm")
    #             )
    #
    #             #перебор тестов
    #             for k in range(help_pos + 1, num_files + 1, step):
    #                 t_det.append(
    #                     self.detect_from_file(f"ORLdataset/s{i}/{k}.pgm")
    #                 )
    #
    #                 # Уменьшение процесса исправления и предусмотр четного/нечетного выбора
    #                 if ch_func == 0:
    #                     jjj = j - 1 + num_e * (i - 1)
    #                     kkk = k - num_e - 1 + (10 - num_e) * (i - 1)
    #                 else:
    #                     jjj = ind_et
    #                     kkk = ind_t
    #
    #                 test_result = self.check_against_test(e_det[jjj], t_det[kkk])
    #                 sum_det += test_result
    #                 stat_det_indv.append(test_result)
    #
    #                 ind_t += 1
    #
    #             ind_et += 1
    #         #ускорение процесса исправления
    #         dif = num_files - num_e
    #         stat_det.append(sum_det / (dif * num_e))
    #
    #     stat_det_indv_n = np.zeros(dif * num_subfolders)
    #
    #     #перебор каждого s
    #     for m in range(1, num_subfolders + 1, 1):
    #         ad = 0
    #
    #         initial = (m-1) * dif
    #         end = dif * m
    #
    #         for l in range(initial, end, 1):
    #             for o in range(0, num_e, 1):
    #                 v = ad + dif * o + (m-1) * num_e * dif
    #                 #расчет среднего показателя тестовых изображений относительно кол-ва эталонов
    #                 stat_det_indv_n[l] += stat_det_indv[v]
    #
    #             ad += 1
    #
    #             stat_det_indv_n[l] = stat_det_indv_n[l] / num_e
    #
    #     return MethodData(self.title, stat_det, stat_det_indv, t_det, e_det, stat_det_indv_n)

    def process_subfolder(self, folder_path, start_pos, end_pos, step, num_e, help_pos, ch_func, folder_index, stat_det_indv,
                          t_det, e_det):
        sum_det = 0
        num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

        for j in range(start_pos, end_pos + 1, step):
            e_det.append(self.detect_from_file(f"{folder_path}/{j}.pgm"))

            for k in range(help_pos + 1, num_files + 1, step):
                t_det.append(self.detect_from_file(f"{folder_path}/{k}.pgm"))

                jjj = (j - 1 + num_e * (folder_index - 1)) if ch_func == 0 else (len(e_det) - 1)
                kkk = (k - num_e - 1 + (10 - num_e) * (folder_index - 1)) if ch_func == 0 else (len(t_det) - 1)

                test_result = self.check_against_test(e_det[jjj], t_det[kkk])
                sum_det += test_result
                stat_det_indv.append(test_result)

        return sum_det, num_files

    def create_chart_data(self, num_e, num_c, start_pos, step, end_pos, ch_func):
        stat_det = []
        stat_det_indv = []
        t_det = []
        e_det = []

        if num_c == 0:
            raise Exception("Missing ORLDatabase")

        help_pos = num_e if ch_func == 0 else 1 if ch_func == 1 else 0

        folder_paths = [f"ORLdataset/s{i}" for i in range(1, num_c + 1)]
        for i, folder_path in enumerate(folder_paths, start=1):
            sum_det, num_files = self.process_subfolder(
                folder_path, start_pos, end_pos, step, num_e, help_pos, ch_func, i, stat_det_indv, t_det, e_det
            )
            dif = num_files - num_e
            stat_det.append(sum_det / (dif * num_e))

        stat_det_indv_n = np.zeros(dif * num_c)
        for m in range(num_c):
            for l in range(dif):
                sum_individual = sum(stat_det_indv[l + dif * o + m * num_e * dif] for o in range(num_e))
                stat_det_indv_n[l + m * dif] = sum_individual / num_e

        return MethodData(self.title, stat_det, stat_det_indv, t_det, e_det, stat_det_indv_n)

    def create_chart_data_from_selected(self, filename1, filename2) -> SelectedFileData:
        e = self.detect_from_selected_file(filename1)
        t = self.detect_from_selected_file(filename2)

        similarity = self.check_against_test(e, t)

        return SelectedFileData(e, t, similarity)

    def create_chart_data_from_folder(self, path, num_e):
        stat_det = []
        stat_det_indv = []
        t_det = []
        e_det = []

        help_pos = num_e
        num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        sum_det, num_files = self.process_subfolder(
            path, 0, num_files, 1, num_e, help_pos, 0, 1, stat_det_indv, t_det, e_det
        )
        dif = num_files - num_e
        stat_det.append(sum_det / (dif * num_e))

        return MethodData(self.title, stat_det, stat_det_indv, t_det, e_det, [])

    def plot_func(self):
        return lambda x: plt.imshow(x, cmap='gray', vmin=0, vmax=255)

    def plot_func_on_axis(self, axis):
        return lambda x: axis.imshow(x, cmap='gray', vmin=0, vmax=255)

    def plot_on_num_ax(self, data, ax_numbered, ax_numbered_2):
        ax_numbered.set_title(f'{data.title}: {round(data.stat_indv[0], 3)}')
        data_to_plot_1 = self.correct_plot_data(data.t[0])
        met_a = self.plot_func_on_axis(ax_numbered)(data_to_plot_1)

        ax_numbered_2.set_title(data.title)
        data_to_plot_2 = self.correct_plot_data(data.e[0])
        a_e = self.plot_func_on_axis(ax_numbered_2)(data_to_plot_2)

        return met_a, a_e

    def init_plot(self, data, ax, ax_ind, ax_numbered, ax_numbered_2):
        self.ax = ax
        self.ax_ind = ax_ind
        self.ax_numbered = ax_numbered
        self.ax_numbered_2 = ax_numbered_2

        ax.set_title(data.title)

        ax.set_xlabel("№ класса")
        ax.set_ylabel("Точность, %")

        ax_ind.set_xlabel("№ теста")
        ax_ind.set_ylabel("Точность, %")

        ax_numbered.set_title(f'{data.title}: {round(data.stat_indv[0], 3)}')

        met_a, a_e = self.plot_on_num_ax(data, ax_numbered, ax_numbered_2)

        x_r = np.arange(len(data.stat))
        x_r_ind = np.arange(len(data.stat_indv_n))

        return PlotData(met_a, a_e, x_r, x_r_ind)

    def plot_stat(self, data, plot_data, current_index):
        self.ax.plot(plot_data.x_r[0:current_index+1:1], data.stat[0:current_index+1:1], color="green")

    def update_numbered_axis(self, data, index):
        self.ax_numbered.set_title(f'{data.title}:{data.stat_indv[index]:.3f}')

    def show_mean(self, plot_data, data, put):
        self.ax_ind.plot(plot_data.x_ind[0:put:1], data.stat_indv_n[0:put:1], color="green")
        self.ax_ind.set_title(data.title)
