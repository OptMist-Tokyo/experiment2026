import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def update_time():
    now = datetime.now()
    label.config(text=now.strftime("%H:%M:%S"))
    
    # アラーム判定
    alarm_h = hour_spin.get().zfill(2)
    alarm_m = min_spin.get().zfill(2)
    if now.strftime("%H") == alarm_h and now.strftime("%M") == alarm_m and now.second == 0:
        trigger_alarm()
    
    root.after(1000, update_time)

def trigger_alarm():
    label.config(fg="red")
    messagebox.showinfo("alerm", f"It's time! ({hour_spin.get()}:{min_spin.get()})")
    label.config(fg="green")

# --- 画面切り替え関数 ---
def show_setting():
    clock_frame.pack_forget()
    setting_frame.pack(fill="both", expand=True) # 画面全体に広げる

def show_clock():
    setting_frame.pack_forget()
    clock_frame.pack(fill="both", expand=True) # 画面全体に広げる

root = tk.Tk()
root.title("Alarm Clock")
# ウィンドウサイズを少し大きめに固定（見失わないように）
root.geometry("600x400")
root.configure(bg="black")

# ================= 1. 時計画面 (clock_frame) =================
clock_frame = tk.Frame(root, bg="black")

# centerに配置するためにプロパティを調整
label = tk.Label(clock_frame, font=("Arial", 80), fg="green", bg="black")
label.pack(expand=True)

btn_setup = tk.Button(clock_frame, text="set alerm time", command=show_setting, 
                      bg="#333", fg="white", font=("Arial", 15), padx=20, pady=10)
btn_setup.pack(pady=20)

clock_frame.pack(fill="both", expand=True) # 初期表示

# ================= 2. 設定画面 (setting_frame) =================
setting_frame = tk.Frame(root, bg="black")

tk.Label(setting_frame, text="set alerm time", font=("Arial", 20), fg="white", bg="black").pack(pady=20)

spin_container = tk.Frame(setting_frame, bg="black")
spin_container.pack(expand=True)

# format="%02.0f" で 01, 02 と表示されるようにする
hour_spin = tk.Spinbox(spin_container, from_=0, to=23, width=3, font=("Arial", 50), format="%02.0f")
hour_spin.pack(side=tk.LEFT, padx=10)

tk.Label(spin_container, text=":", font=("Arial", 50), fg="white", bg="black").pack(side=tk.LEFT)

min_spin = tk.Spinbox(spin_container, from_=0, to=59, width=3, font=("Arial", 50), format="%02.0f")
min_spin.pack(side=tk.LEFT, padx=10)

btn_done = tk.Button(setting_frame, text="set and back to clock", command=show_clock, 
                     bg="green", fg="white", font=("Arial", 15), padx=20, pady=10)
btn_done.pack(pady=30)

# ================= 実行 =================
update_time()
root.mainloop()
