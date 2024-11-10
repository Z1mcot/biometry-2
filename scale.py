from matplotlib import pyplot as plt

from base_detector import BaseDetector
from skimage import transform, metrics, io


class ScaleDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.title = "Scale"

    def detect_from_file(self, path):
        return self.detect(path)

    def detect(self, file):
        img = io.imread(file, as_gray=True)

        # Измененеие размера картинки
        img_res = transform.resize(img, (40, 40))
        return img_res

    def check_against_test(self, ref, tst):
        ssim = metrics.structural_similarity(ref, tst, data_range=255)

        return ssim if ssim <= 1 else 2 - ssim

    def plot_func(self):
        return lambda x: plt.imshow(x, cmap='gray')

    def plot_func_on_axis(self, axis):
        return lambda x: axis.imshow(x, cmap='gray')