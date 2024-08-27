import tkinter as tk
from tkinter import ttk
import random

class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ルーレット")
        self.root.geometry("1000x700")
        self.root.configure(bg="#191970")

        self.choices = ["当たり", "外れ", "外れ", "外れ", "外れ", "外れ"]
        self.labels = []
        self.create_widgets()
        self.running = False
        self.hit_probability = 50  # 初期値: 当たりの確率50%

        # アプリケーション起動時に設定ウインドウを表示
        self.open_settings()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#191970")
        self.frame.pack(expand=True)

        self.arrow_label = tk.Label(self.frame, text="→", font=("Helvetica", 48), bg="#191970", fg="white")
        self.arrow_label.grid(row=2, column=0, padx=(10, 0))  # 矢印を固定の位置に配置

        for i in range(len(self.choices)):
            label = tk.Label(self.frame, text="", font=("Helvetica", 36, "bold"), bg="#191970", fg="white")
            label.grid(row=i, column=1, pady=20)
            self.labels.append(label)

        self.start_button = ttk.Button(self.root, text="スタート", command=self.start_roulette)
        self.start_button.pack(side="left", padx=20, pady=20)

    def start_roulette(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.result = "当たり" if random.randint(1, 100) <= self.hit_probability else "外れ"
        self.scroll_labels(50)  # 初期速度を速く設定

    def scroll_labels(self, delay):
        if self.running:
            self.choices = self.choices[1:] + self.choices[:1]  # リストのアイテムを回転させる
            for i, label in enumerate(self.labels):
                label.config(text=self.choices[i], fg="#00bfff" if self.choices[i] == "当たり" else "#ffb6c1")

            # エージングアニメーション：徐々に遅くする
            new_delay = delay + 5 if delay < 200 else delay
            if new_delay < 200:
                self.scroll_animation = self.root.after(new_delay, self.scroll_labels, new_delay)
            else:
                self.running = False
                self.display_result()

    def display_result(self):
        # 結果を矢印の位置に自然に反映
        while self.labels[2].cget("text") != self.result:
            self.choices = self.choices[1:] + self.choices[:1]
            for i, label in enumerate(self.labels):
                label.config(text=self.choices[i], fg="#00bfff" if self.choices[i] == "当たり" else "#ffb6c1")
        self.start_button.config(state="normal")

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("設定")
        settings_window.geometry("300x200")

        label = tk.Label(settings_window, text="当たりの確率を選択:")
        label.pack(pady=10)

        self.probability_var = tk.IntVar(value=self.hit_probability)
        probability_slider = tk.Scale(settings_window, from_=0, to=100, orient="horizontal", variable=self.probability_var)
        probability_slider.pack(pady=10)

        ok_button = ttk.Button(settings_window, text="OK", command=self.apply_settings)
        ok_button.pack(pady=10)

    def apply_settings(self):
        self.hit_probability = self.probability_var.get()

if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteApp(root)
    root.mainloop()
