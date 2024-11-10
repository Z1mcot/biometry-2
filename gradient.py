import operator

import cv2
import numpy as np
from matplotlib import pyplot as plt

from base_detector import BaseDetector

class GradientDetector(BaseDetector):
    def __init__(self, ksize=3, dx=1, dy=1):
        super().__init__()
        self.title = "Градиент"
        self.ksize = ksize
        self.dx = dx
        self.dy = dy
        self.delta_k = 80

    def __calculate_abs_grad__(self, file) -> (cv2.Mat, cv2.Mat):
        gradient_x = cv2.Sobel(file, cv2.CV_32F, self.dx, 0, ksize=self.ksize)
        gradient_y = cv2.Sobel(file, cv2.CV_32F, 0, self.dy, ksize=self.ksize)

        # Calculate absolute gradients
        abs_gradient_x = cv2.convertScaleAbs(gradient_x)
        abs_gradient_y = cv2.convertScaleAbs(gradient_y)

        return abs_gradient_x, abs_gradient_y

    def correct_plot_data(self, raw_data):
        return raw_data

    def check_against_test(self, ref, tst):
        in_e_g, e_m_g = max(enumerate(ref), key=operator.itemgetter(1))
        t_max_g = tst[in_e_g]
        delta_g = abs(e_m_g - t_max_g)

        return 1 if delta_g < self.delta_k else 0

    def detect(self, file):
        # Calculate absolute gradients
        abs_gradient_x, abs_gradient_y = self.__calculate_abs_grad__(file)

        # Compute final gradient by combining x and y gradients
        gradient = cv2.addWeighted(abs_gradient_x, 0.5, abs_gradient_y, 0.5, 0)
        grad_sum = list(
            map(
                lambda x: round(sum(x) / len(x), 1),
                gradient
            )
        )

        return grad_sum

    def plot_func(self):
        return lambda x: plt.plot(np.arange(len(x)), x, color="green")

    def plot_func_on_axis(self, axis):
        return lambda x: axis.plot(np.arange(len(x)), x, color="green")

    def plot_on_num_ax(self, data, ax_numbered, ax_numbered_2):
        ax_numbered.set_title(data.title)
        data_to_plot = self.correct_plot_data(data.t[0])
        met_a, = self.plot_func_on_axis(ax_numbered)(data_to_plot)
        a_e, = self.plot_func_on_axis(ax_numbered_2)(data_to_plot)

        return met_a, a_e