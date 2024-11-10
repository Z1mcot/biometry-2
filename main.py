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
def build_charts(num_e, start_pos, step, end_pos, ch_func):
    img_data = img_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)
    hist_data = hist_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)
    grad_data = grad_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)
    dft_data = dft_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)
    dct_data = dct_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)
    scale_data = scale_det.create_chart_data(num_e, start_pos, step, end_pos, ch_func)

    plot_drawer.draw_plot(num_e, img_data, hist_data, grad_data, dft_data, dct_data, scale_data)

# Функция получения кол-ва эталонов
def Get_eAmount_func(choosed_op):
    num_etalons = num_etalons_entry.get()
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
        build_charts(int(num_etalons), start_pos, step, end_pos, choosed_op)
    else:
        tk.showerror("Ошибка!", "Должно быть введено целое положительное число!")

# Отображение результата
def Show_Results_func(text):
    msg = text
    mb.showinfo("Результат", msg)

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


# Выбор из доступных действий
plot_button1 = tk.Button(root, text="Обучение", width=40, height=2, pady=10, command=lambda :Get_eAmount_func(int(0)))
plot_button1.pack()
plot_button1.bind("<Enter>", on_enter)
plot_button1.bind("<Leave>", on_leave)
root.mainloop()

