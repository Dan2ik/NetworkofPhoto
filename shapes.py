import math
from tkinter import messagebox

class Circle:
    def __init__(self, canvas, x, y, size=10, color="red", cost=0, equipment_type=""):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.cost = cost  # Стоимость оборудования
        self.equipment_type = equipment_type  # Тип оборудования
        self.lines = []
        self.shape = self.canvas.create_oval(
            x - size, y - size, x + size, y + size, fill=color
        )
        self.label = self.canvas.create_text(x, y + size + 10, text=equipment_type, fill="black")  # Создаем текстовую метку
        self.canvas.tag_bind(self.shape, "<Button-1>", self.select)
        self.canvas.tag_bind(self.shape, "<B1-Motion>", self.move)
        self.canvas.tag_bind(self.shape, "<Button-3>", self.delete)

    def select(self, event):
        """Выделение круга и вывод его информации."""
        self.canvas.tag_raise(self.shape)
        self.canvas.tag_raise(self.label)  # Поднимаем метку над другими объектами
        # messagebox.showinfo(
        #     "Информация об оборудовании",
        #     f"Тип: {self.equipment_type}\nСтоимость: {self.cost} руб."
        # )

    def move(self, event):
        """Перемещение круга и метки."""
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.shape, dx, dy)
        self.canvas.move(self.label, dx, dy)  # Перемещаем метку вместе с кругом
        self.x, self.y = event.x, event.y
        self.update_lines()  # Обновляем линии, связанные с этим кругом

    def delete(self, event=None):
        """Удаление круга, метки и связанных с ним линий."""
        for line in self.lines:
            line.delete()
        self.canvas.delete(self.shape)
        self.canvas.delete(self.label)  # Удаляем метку

    def add_line(self, line):
        """Добавляем линию в список связанных линий."""
        self.lines.append(line)

    def update_lines(self):
        """Обновляем линии, связанные с этим кругом."""
        for line in self.lines:
            line.update_position(self)


class Line:
    def __init__(self, canvas, start_circle, end_circle):
        self.canvas = canvas
        self.start_circle = start_circle
        self.end_circle = end_circle
        self.line = self.canvas.create_line(
            start_circle.x, start_circle.y, end_circle.x, end_circle.y, width=2, fill="blue"
        )
        self.canvas.tag_bind(self.line, "<Button-3>", self.delete)  # Удаление линии по правому клику
        start_circle.add_line(self)  # Добавляем линию в список связанных линий начального круга
        end_circle.add_line(self)  # Добавляем линию в список связанных линий конечного круга

    def delete(self, event=None):
        """Удаление линии."""
        self.canvas.delete(self.line)

    def update_position(self, circle):
        """Обновление позиции линии при перемещении круга."""
        if circle == self.start_circle:
            self.canvas.coords(self.line, circle.x, circle.y, self.end_circle.x, self.end_circle.y)
        elif circle == self.end_circle:
            self.canvas.coords(self.line, self.start_circle.x, self.start_circle.y, circle.x, circle.y)

    def get_length(self):
        """Возвращает длину линии в пикселях."""
        dx = self.end_circle.x - self.start_circle.x
        dy = self.end_circle.y - self.start_circle.y
        return math.sqrt(dx**2 + dy**2)

