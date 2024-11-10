import cv2
import numpy as np

from base_detector import BaseDetector

class DftDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.title = "DFT"

    def detect(self, file):
        # Применение двумерного дискретного преобразования Фурье (DFT)
        dft = cv2.dft(np.float32(file), flags=cv2.DFT_COMPLEX_OUTPUT)

        # Сдвиг нулевых частот в центр (циклическая свертка)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        return magnitude_spectrum

    def correct_plot_data(self, raw_data):
        return np.round(raw_data, decimals=3)

    def check_against_test(self, ref, tst):
        # среднее по эталону, dft
        mean_mag_e = np.mean(ref)
        # среднее по тестовому, dft
        mean_mag_t = np.mean(tst)
        # вычисление процента совпадения
        similarity_percent_dft = mean_mag_t / mean_mag_e
        if similarity_percent_dft > 1:
            similarity_percent_dft = 2 - similarity_percent_dft

        return similarity_percent_dft