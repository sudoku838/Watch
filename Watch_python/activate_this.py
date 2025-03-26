import tkinter as tk
import time
import math
from datetime import datetime

class TrapezoidClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Часы")
        self.canvas = tk.Canvas(root, width=600, height=500, bg='white')
        self.canvas.pack()
        self.setup_ui()
        self.update_clock()

    def setup_ui(self):
        # Рисуем трапецию
        self.canvas.create_polygon(
            100, 350, 500, 350, 400, 50, 200, 50,
            fill='gray', outline='black'
        )

        # Рисуем основание
        self.canvas.create_rectangle(
            80, 350, 520, 390,
            fill='#8B4513', outline='black', width=2
        )

        # Добавляем текстуру дерева на основание
        for i in range(5):
            y = 355 + i * 6
            self.canvas.create_line(85, y, 515, y, fill='#654321', width=1)

        # Рисуем циферблат
        self.clock_center_x = 300
        self.clock_center_y = 200
        self.clock_radius = 120
        self.canvas.create_oval(
            180, 80, 420, 320,
            fill='white', width=3
        )

        # Рисуем цифры на циферблате
        for i in range(1, 13):
            angle = math.radians(-i * 30 + 90)
            self.canvas.create_text(
                300 + 102 * math.cos(angle),
                200 - 102 * math.sin(angle),
                text=str(i),
                font=('Arial', 12)
            )

        # Создаем стрелки
        self.hands = [
            self.canvas.create_line(300, 200, 300, 200, width=4),  # часовая
            self.canvas.create_line(300, 200, 300, 200, width=3, fill='blue'),  # минутная
            self.canvas.create_line(300, 200, 300, 200, width=2, fill='red')   # секундная
        ]

        # Центральная точка
        self.canvas.create_oval(295, 195, 305, 205, fill='black')

        # Отображение даты и года
        current_date = datetime.now().strftime("%d.%m.%Y")
        self.date_text = self.canvas.create_text(
            300, 370,
            text=current_date,
            font=('Arial', 16, 'bold'),
            fill='white'
        )

        # Отображение времени в цифровом формате
        self.digital_time = self.canvas.create_text(
            300, 400,
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
        hour_angle = math.radians(-(hour * 30 + minute * 0.5) + 90)
        minute_angle = math.radians(-minute * 6 + 90)
        second_angle = math.radians(-second * 6 + 90)

        # Длины стрелок
        hour_length = self.clock_radius * 0.5
        minute_length = self.clock_radius * 0.7
        second_length = self.clock_radius * 0.9

        # Обновляем часовую стрелку
        self.canvas.coords(
            self.hands[0],
            self.clock_center_x,
            self.clock_center_y,
            self.clock_center_x + hour_length * math.cos(hour_angle),
            self.clock_center_y - hour_length * math.sin(hour_angle)
        )

        # Обновляем минутную стрелку
        self.canvas.coords(
            self.hands[1],
            self.clock_center_x,
            self.clock_center_y,
            self.clock_center_x + minute_length * math.cos(minute_angle),
            self.clock_center_y - minute_length * math.sin(minute_angle)
        )

        # Обновляем секундную стрелку
        self.canvas.coords(
            self.hands[2],
            self.clock_center_x,
            self.clock_center_y,
            self.clock_center_x + second_length * math.cos(second_angle),
            self.clock_center_y - second_length * math.sin(second_angle)
        )

        # Обновляем цифровое время
        current_time = time.strftime("%H:%M:%S")
        self.canvas.itemconfig(self.digital_time, text=current_time)

        # Планируем следующее обновление
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    clock = TrapezoidClock(root)
    root.mainloop()