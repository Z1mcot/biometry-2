import os

import matplotlib.pyplot as plt

from dct import DctDetector
from dft import DftDetector
from gradient import GradientDetector
from hist import HistDetector
from image_detector import ImageDetector
from method_data import MethodData
from scale import ScaleDetector


def draw_plot(
        num_e: int,
        img_data: MethodData,
        hist_data: MethodData,
        grad_data: MethodData,
        dft_data: MethodData,
        dct_data: MethodData,
        scale_data: MethodData,
):
    fig1, ((ax_img_1, ax_hist_1, ax_dft_1, ax_dct_1, ax_grad_1, ax_scale_1), (ax_img_2, ax_hist_2, ax_dft_2, ax_dct_2, ax_grad_2, ax_scale_2)) = plt.subplots(2, 6)
    fig2, ((ax_ind_h, ax_ind_g, ax_ind_dft, ax_ind_dct, ax_ind_scale), (ax_h, ax_g, ax_dft, ax_dct, ax_scale)) = plt.subplots(2, 5)

    img_det = ImageDetector()
    img_plot_data = img_det.init_plot(img_data, None, None, ax_img_1, ax_img_2)

    h_det = HistDetector()
    h_plot_data = h_det.init_plot(hist_data, ax_h, ax_ind_h, ax_hist_1, ax_hist_2)

    grad_det = GradientDetector()
    grad_plot_data = grad_det.init_plot(grad_data, ax_g, ax_ind_g, ax_grad_1, ax_grad_2)

    dft_det = DftDetector()
    dft_plot_data = dft_det.init_plot(dft_data, ax_dft, ax_ind_dft, ax_dft_1, ax_dft_2)

    dct_det = DctDetector()
    dct_plot_data = dct_det.init_plot(dct_data, ax_dct, ax_ind_dct, ax_dct_1, ax_dct_2)

    scale_det = ScaleDetector()
    scale_plot_data = scale_det.init_plot(scale_data, ax_scale, ax_ind_scale, ax_scale_1, ax_scale_2)

    plt.ion()



    # stat_scale = np.round(stat_scale, decimals=3)
    # ax_6.set_title(f'Scale:{round(stat_scale[0],3)}')
    # sc_a = ax_6.imshow(t_scale[0], cmap='gray')

    #показ фигур
    #fig1.set_size_inches(19, 5)
    fig1.show()
    #fig2.set_size_inches(19, 5)
   # fig2.show()
    #поиск числа подпапок
    num_subfolders = len([f.path for f in os.scandir("Test1") if f.is_dir()])
    #num_subfolders = len([f.path for f in os.scandir("ORLdataset") if f.is_dir()])
    #перебор подпапок

    for t in range(0, num_subfolders, 1):
        h_det.plot_stat(hist_data, h_plot_data, t)
        grad_det.plot_stat(grad_data, grad_plot_data, t)
        dft_det.plot_stat(dft_data, dft_plot_data, t)
        dct_det.plot_stat(dct_data, dct_plot_data, t)
        scale_det.plot_stat(scale_data, scale_plot_data, t)

        index = 0
        start = num_e * t

        for p in range(start, start + num_e, 1):
            img_plot_data.set_a_e(img_data.e[p])
            h_plot_data.set_y_a_e(hist_data.e[p])
            dft_plot_data.set_a_e(dft_data.e[p])
            dct_plot_data.set_a_e(dct_data.e[p])
            grad_plot_data.set_y_a_e(grad_data.e[p])
            scale_plot_data.set_a_e(scale_data.e[p])

            num_files = len([f for f in os.listdir(f"Test1/s{t+1}") if os.path.isfile(os.path.join(f"Test1/s{t}", f))])

            for m in range((0 + p * (num_files - num_e)), (num_files - num_e) * (p + 1), 1):
                img_plot_data.set_met_a(img_data.t[m])
                h_plot_data.set_y_met_a(hist_data.t[m])
                dft_plot_data.set_met_a(dft_data.t[m])
                dct_plot_data.set_met_a(dct_data.t[m])
                grad_plot_data.set_y_met_a(grad_data.t[m])
                scale_plot_data.set_met_a(scale_data.t[m])

                h_det.update_numbered_axis(hist_data, m)
                dft_det.update_numbered_axis(dft_data, m)
                dct_det.update_numbered_axis(dct_data, m)
                grad_det.update_numbered_axis(grad_data, m)
                scale_det.update_numbered_axis(scale_data, m)

                #средний по тестам выводится, если рассмотренны все эталоны и выводится последний тест
                if p+1 == start + num_e:
                    put = index + t * (num_files - num_e) + 1

                    h_det.show_mean(h_plot_data, hist_data, put)
                    grad_det.show_mean(grad_plot_data, grad_data, put)
                    dft_det.show_mean(dft_plot_data, dft_data, put)
                    dct_det.show_mean(dct_plot_data, dct_data, put)
                    scale_det.show_mean(scale_plot_data, scale_data, put)

                    index += 1

                #отрисовка фигур
                fig1.canvas.draw()
                fig1.canvas.flush_events()
               # fig2.canvas.draw()
               # fig2.canvas.flush_events()
    plt.pause(120)
    plt.close()

def draw_selected_plot(title, index, data, draw_func):
    plt.subplot(3, 6, index)
    draw_func(data)
    plt.title(title)