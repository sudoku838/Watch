import tkinter as tk
import time
from datetime import datetime
import math

class TriangleClockWithBase:
    def __init__(self, root):
        self.root = root
        self.root.title("часы")
        self.root.geometry("500x550")

        # Цветовая схема
        self.bg_color = '#f5f5f5'
        self.triangle_color = '#e8d9b5'
        self.base_color = '#8B4513'  # цвет дерева
        self.clock_face_color = '#ffffff'
        self.hand_colors = {
            'hour': '#5a3e36',
            'minute': '#7a5c50',
            'second': '#c88a65'
        }
        self.text_color = '#333333'

        # Создаем холст
        self.canvas = tk.Canvas(root, width=500, height=550, bg=self.bg_color)
        self.canvas.pack()

        # Параметры треугольника
        self.triangle_height = 300
        self.triangle_width = 400
        self.triangle_top = 50
        self.triangle_left = 50

        # Создаем элементы часов
        self.draw_clock()

        # Запускаем обновление времени
        self.update_clock()

    def draw_clock(self):
        # Координаты треугольника
        top_point = (self.triangle_left + self.triangle_width//2, self.triangle_top)
        left_point = (self.triangle_left, self.triangle_top + self.triangle_height)
        right_point = (self.triangle_left + self.triangle_width, self.triangle_top + self.triangle_height)

        # Рисуем треугольный корпус
        self.canvas.create_polygon(
            top_point[0], top_point[1],
            left_point[0], left_point[1],
            right_point[0], right_point[1],
            fill=self.triangle_color, outline='black', width=2
        )

        # Рисуем основание
        base_height = 30
        base_top = self.triangle_top + self.triangle_height
        self.canvas.create_rectangle(
            self.triangle_left - 20, base_top,
            self.triangle_left + self.triangle_width + 20, base_top + base_height,
            fill=self.base_color, outline='black', width=2
        )

        # Добавляем текстуру дерева на основание
        for i in range(5):
            y = base_top + 5 + i * 5
            self.canvas.create_line(
                self.triangle_left - 15, y,
                self.triangle_left + self.triangle_width + 15, y,
                fill='#654321', width=1
            )

        # Центр циферблата (по центру треугольника)
        self.clock_center_x = self.triangle_left + self.triangle_width // 2
        self.clock_center_y = self.triangle_top + self.triangle_height // 2

        # Радиус циферблата (ограничен высотой треугольника)
        self.clock_radius = min(self.triangle_height, self.triangle_width) * 0.35

        # Рисуем циферблат
        self.canvas.create_oval(
            self.clock_center_x - self.clock_radius,
            self.clock_center_y - self.clock_radius,
            self.clock_center_x + self.clock_radius,
            self.clock_center_y + self.clock_radius,
            fill=self.clock_face_color, outline='black', width=2
        )

        # Рисуем метки часов
        for i in range(12):
            angle = math.radians(i * 30 - 90)  # -90 чтобы начать с 12 часов
            inner_radius = self.clock_radius * 0.85
            outer_radius = self.clock_radius

            x1 = self.clock_center_x + inner_radius * math.cos(angle)
            y1 = self.clock_center_y + inner_radius * math.sin(angle)
            x2 = self.clock_center_x + outer_radius * math.cos(angle)
            y2 = self.clock_center_y + outer_radius * math.sin(angle)

            self.canvas.create_line(x1, y1, x2, y2, width=2)

        # Создаем стрелки
        self.hands = {
            'hour': self.canvas.create_line(
                self.clock_center_x, self.clock_center_y,
                self.clock_center_x, self.clock_center_y - self.clock_radius * 0.5,
                width=6, fill=self.hand_colors['hour'], capstyle=tk.ROUND
            ),
            'minute': self.canvas.create_line(
                self.clock_center_x, self.clock_center_y,
                self.clock_center_x, self.clock_center_y - self.clock_radius * 0.7,
                width=4, fill=self.hand_colors['minute'], capstyle=tk.ROUND
            ),
            'second': self.canvas.create_line(
                self.clock_center_x, self.clock_center_y,
                self.clock_center_x, self.clock_center_y - self.clock_radius * 0.9,
                width=2, fill=self.hand_colors['second'], capstyle=tk.ROUND
            )
        }

        # Центральная точка
        self.canvas.create_oval(
            self.clock_center_x - 5, self.clock_center_y - 5,
            self.clock_center_x + 5, self.clock_center_y + 5,
            fill=self.hand_colors['second'], outline='black'
        )

        # Текущий год на основании
        current_year = datetime.now().strftime("%Y")
        self.year_text = self.canvas.create_text(
            self.clock_center_x, base_top + base_height//2 - 10,
            text=current_year,
            font=('Times New Roman', 18, 'bold'),
            fill='white'
        )

        # Точное время на основании
        self.time_text = self.canvas.create_text(
            self.clock_center_x, base_top + base_height//2 + 10,
            text="",
            font=('Courier', 14, 'bold'),
            fill='white'
        )

    def update_clock(self):
        now = time.localtime()
        hour = now.tm_hour % 12
        minute = now.tm_min
        second = now.tm_sec

        # Обновляем стрелки
        angles = {
            'hour': math.radians(hour * 30 + minute * 0.5 - 90),
            'minute': math.radians(minute * 6 - 90),
            'second': math.radians(second * 6 - 90)
        }

        for hand_type in self.hands:
            length = self.clock_radius * 0.5 if hand_type == 'hour' else \
                self.clock_radius * 0.7 if hand_type == 'minute' else \
                    self.clock_radius * 0.9

            end_x = self.clock_center_x + length * math.cos(angles[hand_type])
            end_y = self.clock_center_y + length * math.sin(angles[hand_type])

            self.canvas.coords(
                self.hands[hand_type],
                self.clock_center_x, self.clock_center_y, end_x, end_y
            )

        # Обновляем цифровое время на основании
        current_time = time.strftime("%H:%M:%S")
        self.canvas.itemconfig(self.time_text, text=current_time)

        # Планируем следующее обновление
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = TriangleClockWithBase(root)
    root.mainloop()