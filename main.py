import cv2
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import plot_drawer

from dct import DctDetector
from dft import DftDetector
from gradient import GradientDetector
from hist import HistDetector
from image_detector import ImageDetector
from scale import ScaleDetector

img_det = ImageDetector()
hist_det = HistDetector()
grad_det = GradientDetector()
dft_det = DftDetector()
dct_det = DctDetector()
scale_det = ScaleDetector()

# Функция построения графиков
def build_charts(num_e, num_c, start_pos, step, end_pos, ch_func):
    img_data = img_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)
    hist_data = hist_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)
    grad_data = grad_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)
    dft_data = dft_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)
    dct_data = dct_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)
    scale_data = scale_det.create_chart_data(num_e, num_c, start_pos, step, end_pos, ch_func)

    plot_drawer.draw_plot(num_e, num_c, img_data, hist_data, grad_data, dft_data, dct_data, scale_data)

# Построение графиков через выбранные файлы
def build_charts_from_selected(filename1, filename2):
    # delta_k_h = 100
    # delta_k_g = 80
    # res_h = 0
    # res_g = 0
    # sum_sim_dft = 0
    # sum_sim_dct = 0

    img_data = img_det.create_chart_data_from_selected(filename1, filename2)
    hist_data = hist_det.create_chart_data_from_selected(filename1, filename2)
    grad_data = grad_det.create_chart_data_from_selected(filename1, filename2)
    dft_data = dft_det.create_chart_data_from_selected(filename1, filename2)
    dct_data = dct_det.create_chart_data_from_selected(filename1, filename2)
    scale_data = scale_det.create_chart_data_from_selected(filename1, filename2)

    t_or_img = plt.imread(filename2, cv2.IMREAD_GRAYSCALE)
    e_or_img = plt.imread(filename1, cv2.IMREAD_GRAYSCALE)

    plot_drawer.draw_selected_plot("Эталон", 13, e_or_img, img_det.plot_func())
    plot_drawer.draw_selected_plot("Гистограмма", 14, hist_data.e, hist_det.plot_func())

    plot_drawer.draw_selected_plot("DFT", 15, dft_data.e, dft_det.plot_func())
    plot_drawer.draw_selected_plot("DCT", 16, dct_data.e, dct_det.plot_func())

    plot_drawer.draw_selected_plot("Градиент", 17, grad_data.e, grad_det.plot_func())
    plot_drawer.draw_selected_plot("Scale", 18, scale_data.e, scale_det.plot_func())

    plot_drawer.draw_selected_plot("Тест", 1, t_or_img, img_det.plot_func())
    plot_drawer.draw_selected_plot("Гистограмма", 12, hist_data.t, hist_det.plot_func())

    plot_drawer.draw_selected_plot("DFT", 3, dft_data.t, dft_det.plot_func())
    plot_drawer.draw_selected_plot("DCT", 4, dct_data.t, dct_det.plot_func())

    plot_drawer.draw_selected_plot("Градиент", 5, grad_data.t, grad_det.plot_func())
    plot_drawer.draw_selected_plot("Scale", 6, scale_data.t, scale_det.plot_func())

    if (grad_data.similarity != 0
            and hist_data.similarity != 0
            and dft_data.similarity >= 0.5
            and dct_data.similarity >= 0.5
            and scale_data.similarity >= 0.5):
        Show_Results_func("Найдено совпадение")
    else:
        Show_Results_func("Совпадений нет.")

    plt.show()

# Построение графиков кросс-валидации по файлу и числу эталонов
def build_charts_from_given_folder(path, num_e):
    img_data = img_det.create_chart_data_from_folder(path, num_e)
    hist_data = hist_det.create_chart_data_from_folder(path, num_e)
    grad_data = grad_det.create_chart_data_from_folder(path, num_e)
    dft_data = dft_det.create_chart_data_from_folder(path, num_e)
    dct_data = dct_det.create_chart_data_from_folder(path, num_e)
    scale_data = scale_det.create_chart_data_from_folder(path, num_e)

    plot_drawer.draw_plot(num_e, 1, img_data, hist_data, grad_data, dft_data, dct_data, scale_data)


# Функция получения кол-ва эталонов
def Get_eAmount_func(choosed_op):
    num_etalons = num_etalons_entry.get()
    num_classes = num_classes_entry.get()
    if (choosed_op == 0):  # случай 1. Эталоны берутся по порядку
        start_pos = 1
        step = 1
        end_pos = int(num_etalons)
    if (choosed_op == 1):  # случай 2. Эталоны нечётные
        start_pos = 1
        step = 2
        end_pos = 10
        num_etalons = str(5)
    if (choosed_op == 2):  # случай 3. Эталоны чётные
        start_pos = 2
        step = 2
        end_pos = 10
        num_etalons = str(5)
    if num_etalons.isdigit() and int(num_etalons) > 0:  # случай 4. Проверка условия ввода
        build_charts(int(num_etalons), int(num_classes), start_pos, step, end_pos, choosed_op)
    else:
        tk.showerror("Ошибка!", "Должно быть введено целое положительное число!")

# Выбор тестовых
def Select_Test_func(e_n, filename1):
    num_etalons = e_n
    if num_etalons.isdigit() and int(num_etalons) > 0:
        build_charts_from_given_folder(filename1, int(num_etalons))
    else:
        tk.showerror("WARNING", "Должно быть введено целое целое положительное число")

# Файловый диалог
def Select_Activation_func():
    filename1 = fd.askopenfilename()
    filename2 = fd.askopenfilename()
    build_charts_from_selected(filename1, filename2)

# Отображение результата
def Show_Results_func(text):
    msg = text
    mb.showinfo("Результат", msg)

# Кросс-валидация
def Select_CrossValidation():
    root1 = tk.Tk()
    root1.geometry('300x150')
    plot_button2 = tk.Button(root1, text="Нечетные эталоны",
                             command=lambda: Get_eAmount_func(int(1)))
    plot_button2.pack()
    plot_button3 = tk.Button(root1, text="Четные эталоны", command=lambda: Get_eAmount_func(int(2)))
    plot_button3.pack()

# Смена цвета для кнопок при наведении
def on_enter(e):
    e.widget['background'] = 'blue'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

# Главное окно
root = tk.Tk()
root.geometry("640x400")
root.title("Face Recognition System")
# Задание параметров
num_etalons_label = tk.Label(root, text="Введите кол-во эталонов:", font='Times 12')
num_etalons_label.pack()
num_etalons_entry = tk.Entry(root)
num_etalons_entry.pack()

num_classes_label = tk.Label(root, text="Введите кол-во классов сравнения:", font='Times 12')
num_classes_label.pack()
num_classes_entry = tk.Entry(root)
num_classes_entry.pack()


# Выбор из доступных действий
plot_button1 = tk.Button(root, text="Обучение", width=40, height=2, pady=10, command=lambda :Get_eAmount_func(int(0)))
plot_button1.pack()
plot_button1.bind("<Enter>", on_enter)
plot_button1.bind("<Leave>", on_leave)
plot_button2 = tk.Button(root, text="Выбрать изображения", width=40, height=2, pady=10, command=Select_Activation_func)
plot_button2.pack()
plot_button2.bind("<Enter>", on_enter)
plot_button2.bind("<Leave>", on_leave)
plot_button4 = tk.Button(root, text="Кросс-валидация", width=40, height=2, pady=10, command=Select_CrossValidation)
plot_button4.pack()
plot_button4.bind("<Enter>", on_enter)
plot_button4.bind("<Leave>", on_leave)
root.mainloop()

