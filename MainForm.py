# main.py
from tkinter import Tk, Canvas, filedialog
from PIL import ImageGrab, Image, ImageOps
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from shapes import Circle, Line  # Импортируем классы Circle и Line
from tkinter import simpledialog, ttk

EQUIPMENT_TYPES = {
    "Точка доступа Wi-Fi": "blue",
    "Маршрутизатор": "green",
    "Коммутатор": "orange",
    "Сервер": "purple",
    "Крепление кабеля": "gray",
}

class EquipmentDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Добавить оборудование")
        self.geometry("300x300")
        self.parent = parent

        # Комбобокс для выбора типа оборудования
        self.equipment_label = tk.Label(self, text="Выберите тип оборудования:")
        self.equipment_label.pack(pady=5)

        self.equipment_combobox = ttk.Combobox(self, values=list(EQUIPMENT_TYPES.keys()), state="readonly")
        self.equipment_combobox.current(0)  # Устанавливаем первый тип по умолчанию
        self.equipment_combobox.pack(pady=5)

        # Поле для ввода стоимости
        self.cost_label = tk.Label(self, text="Введите стоимость оборудования (руб.):")
        self.cost_label.pack(pady=5)

        self.cost_entry = tk.Entry(self)
        self.cost_entry.pack(pady=5)

        # Кнопка "ОК"
        self.ok_button = tk.Button(self, text="ОК", command=self.on_ok)
        self.ok_button.pack(pady=10)

        # Переменные для хранения результата
        self.equipment_type = None
        self.cost = None

    def on_ok(self):
        """Обработчик нажатия кнопки ОК."""
        try:
            self.equipment_type = self.equipment_combobox.get()
            self.cost = float(self.cost_entry.get())
            self.destroy()  # Закрываем окно
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную стоимость.")

    def show(self):
        """Показывает окно и возвращает результат."""
        self.wait_window()  # Ждем, пока окно не закроется
        return self.equipment_type, self.cost

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Главное окно")
        self.geometry("1400x600")

        # Верхнее меню
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Пункт "О программе"
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=about_menu)

        # Создаем левую панель для кнопок
        left_panel = tk.Frame(self, bg="lightgray", width=150)
        left_panel.pack(side="left", fill="y")

        # Кнопка "Проект"
        project_button = tk.Button(left_panel, text="Проект", command=lambda: self.show_menu(self.project_menu))
        project_button.pack(pady=10, padx=10, fill="x")

        # Создаем выпадающее меню для "Проект" (скрыто по умолчанию)
        self.project_menu = tk.Frame(left_panel, bg="white")
        self.project_menu.pack_forget()  # Скрываем меню

        # Подпункты для "Проект"
        load_button = tk.Button(self.project_menu, text="Загрузить", command=self.load_image)
        load_button.pack(pady=5, padx=20, fill="x")

        save_button = tk.Button(self.project_menu, text="Сохранить", command=self.save_project)
        save_button.pack(pady=5, padx=20, fill="x")

        # Кнопка "Оборудование"
        equipment_button = tk.Button(left_panel, text="Оборудование", command=lambda: self.show_menu(self.equipment_menu))
        equipment_button.pack(pady=10, padx=10, fill="x")

        # Создаем выпадающее меню для "Оборудование" (скрыто по умолчанию)
        self.equipment_menu = tk.Frame(left_panel, bg="white")
        self.equipment_menu.pack_forget()  # Скрываем меню

        # Подпункты для "Оборудование"
        equipment_1_button = tk.Button(self.equipment_menu, text="Добавить оборудование", command=self.start_circle_creation)
        equipment_1_button.pack(pady=5, padx=20, fill="x")

        equipment_3_button = tk.Button(self.equipment_menu, text="Добавление провода связи между точками (нужно нажать на одну точку потом на вторую)", command=self.start_line_creation)
        equipment_3_button.pack(pady=5, padx=20, fill="x")

        # Кнопка "Расчет" (без подпунктов)
        calculation_button = tk.Button(left_panel, text="Расчет", command=self.calculation)
        calculation_button.pack(pady=10, padx=10, fill="x")

        # Основная область окна
        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", expand=True, fill="both")

        # Холст для отображения изображения и фигур
        self.canvas = tk.Canvas(self.main_area, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Переменные для создания кругов и линий
        self.circles = []  # Список всех кругов
        self.selected_circles = []  # Список выбранных кругов для создания линии
        self.is_creating_circle = False  # Флаг для создания круга
        self.is_creating_line = False  # Флаг для создания линии

    def show_menu(self, menu_to_show):
        # Скрываем все выпадающие меню
        self.project_menu.pack_forget()
        self.equipment_menu.pack_forget()

        # Показываем выбранное меню, если оно было скрыто
        if not menu_to_show.winfo_ismapped():
            menu_to_show.pack()

    def show_about(self):
        # Показываем информацию о программе
        messagebox.showinfo("О программе", "Это пример программы с меню и кнопками.")

    def load_image(self):
        # Открываем диалог выбора файла
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png;*.jpg;")]
        )

        if file_path:
            try:
                # Открываем изображение с помощью Pillow
                image = Image.open(file_path)

                # Масштабируем изображение
                image.thumbnail((1000, 1000))

                # Преобразуем изображение в формат, подходящий для tkinter
                tk_image = ImageTk.PhotoImage(image)

                # Отображаем изображение на холсте
                self.canvas.delete("all")  # Очищаем холст перед загрузкой нового изображения
                self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw", image=tk_image)
                self.canvas.image = tk_image  # Сохраняем ссылку, чтобы изображение не удалялось сборщиком мусора

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def start_circle_creation(self):
        """Начинает процесс создания круга."""
        self.is_creating_circle = True
        self.canvas.bind("<Button-1>", self.add_circle)

    def add_circle(self, event):
        """Добавляет круг на холст."""
        if self.is_creating_circle:
            # Открываем кастомное диалоговое окно
            dialog = EquipmentDialog(self)
            equipment_type, cost = dialog.show()

            if equipment_type and cost is not None:
                # Получаем цвет для выбранного типа оборудования
                color = EQUIPMENT_TYPES[equipment_type]

                # Создаем круг с выбранным цветом и стоимостью
                circle = Circle(self.canvas, event.x, event.y, color=color, cost=cost, equipment_type=equipment_type)
                self.circles.append(circle)

                self.is_creating_circle = False
                self.canvas.unbind("<Button-1>")  # Отключаем обработчик кликов
            else:
                # Если пользователь отменил ввод, выходим из режима создания круга
                self.is_creating_circle = False
                self.canvas.unbind("<Button-1>")

    def start_line_creation(self):
        """Начинает процесс создания линии."""
        self.is_creating_line = True
        self.selected_circles = []  # Очищаем список выбранных кругов
        self.canvas.bind("<Button-1>", self.select_circle_for_line)

    def select_circle_for_line(self, event):
        """Выбирает круг для создания линии."""
        if self.is_creating_line:
            # Ищем круг, по которому кликнули
            for circle in self.circles:
                if (circle.x - circle.size <= event.x <= circle.x + circle.size and
                    circle.y - circle.size <= event.y <= circle.y + circle.size):
                    self.selected_circles.append(circle)
                    break

            if len(self.selected_circles) == 2:
                # Создаем линию между двумя выбранными кругами
                line = Line(self.canvas, self.selected_circles[0], self.selected_circles[1])
                self.selected_circles = []  # Очищаем список выбранных кругов
                self.is_creating_line = False
                self.canvas.unbind("<Button-1>")  # Отключаем обработчик кликов

    def save_project(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Сохранить как"
        )
        if not file_path:
            return

        # Экспортируем canvas в PostScript
        ps_path = file_path + ".ps"
        self.canvas.postscript(file=ps_path, colormode="color")

        # Конвертируем PostScript в PNG
        img = Image.open(ps_path)
        img = ImageOps.invert(img.convert("RGB"))  # Инвертируем цвета, если нужно
        img.save(file_path, "png")
        print(f"Canvas сохранен в {file_path}")
        report_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("txt files", "*.txt"), ("All files", "*.*")],
            title="Сохранить как"
        )
        if not file_path:
            return
        self.project_menu.pack_forget()
        self.equipment_menu.pack_forget()
        print("Расчет")
        total_length = 0  # Общая длина кабеля в пикселях
        total_cost = 2  # Общая стоимость кабеля
        total_equipment = 0  # Общая стоимость оборудования

        # Проходим по всем линиям на холсте,
        for circle in self.circles:
            total_equipment += circle.cost
            for line in circle.lines:
                total_length += line.get_length()

        # Переводим длину из пикселей в метры (предположим, что 80 пикселей = 1 метр)
        total_length_meters = total_length / 80

        # Рассчитываем общую стоимость
        total_cost = total_length_meters * 40
        equipment_count = {}  # Счетчик оборудования
        for circle in self.circles:
            if circle.equipment_type in equipment_count:
                equipment_count[circle.equipment_type] += 1
            else:
                equipment_count[circle.equipment_type] = 1
            total_cost += circle.cost
        with open(report_path, "w", encoding="utf-8") as file:
            file.write("=== ОТЧЕТ ПО ПРОЕКТУ ===\n")
            file.write(f"Общая длина кабеля: {total_length_meters:.2f} метров\n")
            file.write(f"Стоимость кабеля: {total_cost:.2f} руб.\n")
            file.write("\nИспользованное оборудование:\n")
            for eq_type, count in equipment_count.items():
                file.write(f"- {eq_type}: {count} шт.\n")
            file.write(f"\nОбщая стоимость проекта: {total_equipment + total_cost} руб.\n")
        # Выводим результат

    def calculation(self):
        self.project_menu.pack_forget()
        self.equipment_menu.pack_forget()
        print("Расчет")
        total_length = 0  # Общая длина кабеля в пикселях
        total_cost = 2    # Общая стоимость кабеля
        total_equipment = 0  # Общая стоимость оборудования

        # Проходим по всем линиям на холсте,
        for circle in self.circles:
            total_equipment += circle.cost
            for line in circle.lines:
                total_length += line.get_length()

        # Переводим длину из пикселей в метры (предположим, что 80 пикселей = 1 метр)
        total_length_meters = total_length / 80

        # Рассчитываем общую стоимость
        total_cost = total_length_meters * 40

        # Выводим результат
        messagebox.showinfo(
            "Результат расчета",
            f"Общая длина кабеля: {total_length_meters:.2f} м\n"
            f"Стоимость кабеля: {total_cost:.2f} руб.\n"
            f"Стоимость оборудования: {total_equipment:.2f} руб.\n"
            f"Стоимость общая: {total_equipment + total_cost:.2f} руб."
        )