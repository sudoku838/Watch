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
        self.canvas.create_polygon(
            100, 350, 500, 350, 400, 50, 200, 50,
            fill='gray', outline='black'
        )
        #основание
        self.canvas.create_rectangle(
            80, 350, 520, 390,
            fill='#8B4513', outline='black', width=2
        )
        for i in range(5):
            y = 355 + i * 6
            self.canvas.create_line(85, y, 515, y, fill='#654321', width=1)
            #циферблат
        self.clock_center_x = 300
        self.clock_center_y = 200
        self.clock_radius = 120
        self.canvas.create_oval(
            180, 80, 420, 320,
            fill='white', width=3
        )
        for i in range(1, 13):
            angle = math.radians(-i * 30 + 90)
            self.canvas.create_text(
                300 + 102 * math.cos(angle),
                200 - 102 * math.sin(angle),
                text=str(i),
                font=('Arial', 12)
            )
        self.hand_elements = {
            'hour': {
                'line': None,
                'triangle': None,
                'base_circle': None
            },
            'minute': {
                'line': None,
                'triangle': None,
                'base_circle': None
            },
            'second': {
                'line': None,
                'triangle': None,
                'base_circle': None
            }
        }
        self.canvas.create_oval(295, 195, 305, 205, fill='black')
        current_date = datetime.now().strftime("%d.%m.%Y")
        self.date_text = self.canvas.create_text(
            300, 370,
            text=current_date,
            font=('Arial', 16, 'bold'),
            fill='white'
        )
        self.digital_time = self.canvas.create_text(
            300, 400,
            text="",
            font=('Courier', 14, 'bold'),
            fill='white'
        )

    def create_arrowhead(self, x, y, angle, size, color):
        angle_rad = math.radians(angle)
        x1 = x - size * math.cos(angle_rad + math.pi/2)
        y1 = y + size * math.sin(angle_rad + math.pi/2)
        x2 = x - size * math.cos(angle_rad - math.pi/2)
        y2 = y + size * math.sin(angle_rad - math.pi/2)
        return self.canvas.create_polygon(x, y, x1, y1, x2, y2, fill=color)

    def update_clock(self):
        now = time.localtime()
        hour = now.tm_hour % 12
        minute = now.tm_min
        second = now.tm_sec
        for hand_type in self.hand_elements.values():
            for element in hand_type.values():
                if element:
                    self.canvas.delete(element)
        hour_length = self.clock_radius * 0.5
        minute_length = self.clock_radius * 0.7
        second_length = self.clock_radius * 0.9
        hour_angle = math.radians(-(hour * 30 + minute * 0.5) + 90)
        minute_angle = math.radians(-minute * 6 + 90)
        second_angle = math.radians(-second * 6 + 90)
        hour_x = self.clock_center_x + hour_length * math.cos(hour_angle)
        hour_y = self.clock_center_y - hour_length * math.sin(hour_angle)
        minute_x = self.clock_center_x + minute_length * math.cos(minute_angle)
        minute_y = self.clock_center_y - minute_length * math.sin(minute_angle)
        second_x = self.clock_center_x + second_length * math.cos(second_angle)
        second_y = self.clock_center_y - second_length * math.sin(second_angle)
        self.hand_elements['hour']['line'] = self.canvas.create_line(
            self.clock_center_x, self.clock_center_y, hour_x, hour_y,
            width=6, fill='darkgreen', capstyle=tk.ROUND
        )
        self.hand_elements['hour']['triangle'] = self.create_arrowhead(
            hour_x, hour_y, math.degrees(hour_angle), 10, 'darkgreen'
        )
        self.hand_elements['hour']['base_circle'] = self.canvas.create_oval(
            self.clock_center_x - 8, self.clock_center_y - 8,
            self.clock_center_x + 8, self.clock_center_y + 8,
            fill='darkgreen', outline='black'
        )
        self.hand_elements['minute']['line'] = self.canvas.create_line(
            self.clock_center_x, self.clock_center_y, minute_x, minute_y,
            width=4, fill='darkblue', capstyle=tk.ROUND
        )
        self.hand_elements['minute']['triangle'] = self.create_arrowhead(
            minute_x, minute_y, math.degrees(minute_angle), 8, 'darkblue'
        )
        self.hand_elements['minute']['base_circle'] = self.canvas.create_oval(
            self.clock_center_x - 6, self.clock_center_y - 6,
            self.clock_center_x + 6, self.clock_center_y + 6,
            fill='darkblue', outline='black'
        )
        self.hand_elements['second']['line'] = self.canvas.create_line(
            self.clock_center_x, self.clock_center_y, second_x, second_y,
            width=2, fill='darkred', capstyle=tk.ROUND
        )
        self.hand_elements['second']['triangle'] = self.create_arrowhead(
            second_x, second_y, math.degrees(second_angle), 6, 'darkred'
        )
        self.hand_elements['second']['base_circle'] = self.canvas.create_oval(
            self.clock_center_x - 4, self.clock_center_y - 4,
            self.clock_center_x + 4, self.clock_center_y + 4,
            fill='darkred', outline='black'
        )
        current_time = time.strftime("%H:%M:%S")
        self.canvas.itemconfig(self.digital_time, text=current_time)
        self.root.after(1000, self.update_clock)
if __name__ == "__main__":
    root = tk.Tk()
    clock = TrapezoidClock(root)
    root.mainloop()
