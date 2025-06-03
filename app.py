import tkinter as tk
from tkinter import messagebox
import time
import threading
try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер обратного отсчёта")

        self.running = False
        self.paused = False
        self.remaining = 0

        self.entry = tk.Entry(root, width=20, font=("Arial", 14))
        self.entry.insert(0, "1:00")  
        self.entry.pack(pady=10)

        self.label = tk.Label(root, text="00:00", font=("Arial", 40))
        self.label.pack(pady=20)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="Старт", width=10, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = tk.Button(btn_frame, text="Пауза", width=10, command=self.pause)
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Сброс", width=10, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=5)

    def parse_input(self):
        input_str = self.entry.get()
        try:
            if ":" in input_str:
                minutes, seconds = map(int, input_str.split(":"))
                return minutes * 60 + seconds
            else:
                return int(input_str)
        except:
            messagebox.showerror("Ошибка", "Введите время в формате MM:SS или только секунды.")
            return 0

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02}:{s:02}"

    def update_display(self):
        self.label.config(text=self.format_time(self.remaining))

    def countdown(self):
        while self.running and self.remaining > 0:
            if not self.paused:
                time.sleep(1)
                self.remaining -= 1
                self.update_display()
        if self.remaining == 0 and self.running:
            self.running = False
            self.update_display()
            self.time_up()

    def start(self):
        if not self.running:
            self.remaining = self.parse_input()
            if self.remaining <= 0:
                return
            self.running = True
            self.paused = False
            threading.Thread(target=self.countdown, daemon=True).start()
        else:
            self.paused = False

    def pause(self):
        if self.running:
            self.paused = True

    def reset(self):
        self.running = False
        self.paused = False
        self.remaining = 0
        self.update_display()

    def time_up(self):
        if SOUND_ENABLED:
            playsound("alarm.mp3")  
        else:
            messagebox.showinfo("Время вышло", "Обратный отсчёт завершён!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
