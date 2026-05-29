import tkinter as tk
from datetime import datetime
from time import sleep, time
import threading
import atexit

import spidev
from gpiozero import PWMOutputDevice, OutputDevice, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

# =====================================================================
#  ハードウェア初期化
# =====================================================================
buzzer = PWMOutputDevice(17)

servo_factory = PiGPIOFactory()
servo = AngularServo(
    18,
    min_angle=-90,
    max_angle=90,
    min_pulse_width=0.0005,
    max_pulse_width=0.0024,
    initial_angle=0,
    pin_factory=servo_factory,
)

sensor_power = OutputDevice(26)
sensor_power.on()

spi = spidev.SpiDev()
spi.open(1, 2)
spi.max_speed_hz = 1350000


def cleanup():
    try:
        buzzer.off()
    except Exception:
        pass
    try:
        servo.detach()
    except Exception:
        pass
    try:
        spi.close()
    except Exception:
        pass
    try:
        sensor_power.off()
    except Exception:
        pass


atexit.register(cleanup)


# =====================================================================
#  ブザー制御
# =====================================================================
def play_tone(frequency, volume):
    buzzer.frequency = frequency
    buzzer.value = volume / 2


def stop_tone():
    buzzer.value = 0


def buzz_once(stop_event):
    for _ in range(10):
        for _ in range(2):
            if stop_event.is_set():
                stop_tone()
                return
            play_tone(3200, 0.5)
            sleep(0.1)
            stop_tone()
            sleep(0.05)
        for _ in range(12):
            if stop_event.is_set():
                return
            sleep(0.05)


def buzz_loop(stop_event):
    while not stop_event.is_set():
        buzz_once(stop_event)
    stop_tone()


# =====================================================================
#  圧力センサー
# =====================================================================
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    command = [1, (8 + channel) << 4, 0]
    adc = spi.xfer2(command)
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def is_awake(threshold=300, check_duration=3.0, interval=0.2):
    print("🛏️ センサーでベッドの状態を確認中...")
    empty_count = 0
    total_checks = 0
    start_time = time()
    while time() - start_time < check_duration:
        val = read_adc(0)
        print("[測定中] 現在の圧力値: {:4d}".format(val))
        if val < threshold:
            empty_count += 1
        total_checks += 1
        sleep(interval)
    result = empty_count >= (total_checks / 2)
    print("✅ 起床確認" if result else "💤 まだ就寝中")
    return result


# =====================================================================
#  ハンマー制御
# =====================================================================
def hammer_strike(times, stop_event):
    servo.angle = 90
    sleep(0.5)
    for i in range(times):
        if stop_event.is_set():
            break
        print("ピコッ！！（振り下ろす） {}/{}".format(i + 1, times))
        servo.angle = 0
        sleep(0.3)
        servo.angle = 90
        sleep(0.3)
    servo.angle = 0


# =====================================================================
#  アラームシーケンス（更新後フローチャート）
#
#  n ← 0
#      ↓
#  [圧力チェック] ←─────────────────────────────┐
#      ↓ 起きていたら → [finish]                  │
#      ↓ 寝ている                                  │
#  [ブザーON]                                     │
#      ↓                                          │
#  [Dismiss押下 or 30秒経過]                       │
#      ↓                                          │
#  [ブザーOFF → 1分待機]                          │
#      ↓                                          │
#  [beat: n*10回叩く(ブザーON継続)]                │
#      ↓                                          │
#  [n++]                                          │
#      └──────────────────────────────────────────┘
# =====================================================================
stop_event = None
snooze_event = None
alarm_thread = None


def alarm_sequence(stop_ev, snooze_ev, on_finish):
    """
    stop_ev  : Dismiss は使わない。起床確認時にセットして全停止
    snooze_ev: アラーム画面の「Dismiss」ボタン押下で30秒待ちをスキップ
    on_finish: シーケンス終了時のGUIコールバック
    """
    n = 0  # 周回カウンタ。beat回数は n*10
    try:
        while not stop_ev.is_set():

            # ── ステップ1: 圧力チェック ──────────────────────
            if is_awake():
                print("✅ 起床確認。叩かず終了 (n={})".format(n))
                stop_ev.set()
                break

            # ── ステップ2: ブザーON ──────────────────────────
            buzz_stop = threading.Event()
            buzz_thread = threading.Thread(
                target=buzz_loop, args=(buzz_stop,), daemon=True
            )
            buzz_thread.start()
            print("🔔 ブザーON (周回 n={})".format(n))

            # ── ステップ3: 30秒待つ(Dismissで早送り可) ────────
            snooze_ev.clear()
            wait_start = time()
            while time() - wait_start < 30:
                if stop_ev.is_set():
                    break
                if snooze_ev.is_set():
                    print("💤 Dismiss押下: 30秒待ちをスキップ")
                    break
                sleep(0.1)

            if stop_ev.is_set():
                buzz_stop.set()
                buzz_thread.join(timeout=3)
                break

            # ── ステップ4: ブザーOFF → 1分待機 ───────────────
            print("🔕 ブザーOFF → 1分待機")
            buzz_stop.set()
            buzz_thread.join(timeout=3)

            wait_start = time()
            while time() - wait_start < 60:
                if stop_ev.is_set():
                    break
                sleep(0.1)

            if stop_ev.is_set():
                break

            # ── ステップ5: beat (n*10回叩く、ブザーON継続) ───
            beat_count = n * 10
            if beat_count > 0:
                print("⏰ ブザー＋ハンマー {}回".format(beat_count))
                buzz_stop = threading.Event()
                buzz_thread = threading.Thread(
                    target=buzz_loop, args=(buzz_stop,), daemon=True
                )
                buzz_thread.start()

                hammer_strike(beat_count, stop_ev)

                buzz_stop.set()
                buzz_thread.join(timeout=3)
            else:
                print("⏰ 1周目につき叩かない (n=0)")

            # ── ステップ6: n++ ───────────────────────────────
            n += 1

            # ループ先頭(圧力チェック)へ戻る

    finally:
        stop_tone()
        try:
            servo.angle = 0
        except Exception:
            pass
        on_finish()


# =====================================================================
#  GUI
# =====================================================================
last_fired_minute = None


def update_time():
    global last_fired_minute
    now = datetime.now()
    time_label.config(text=now.strftime("%H:%M:%S"))

    alarm_h = hour_spin.get().zfill(2)
    alarm_m = min_spin.get().zfill(2)
    current_minute = now.strftime("%H:%M")
    alarm_minute   = "{}:{}".format(alarm_h, alarm_m)

    if (current_minute == alarm_minute
            and current_minute != last_fired_minute
            and (alarm_thread is None or not alarm_thread.is_alive())):
        last_fired_minute = current_minute
        trigger_alarm()

    root.after(200, update_time)


def trigger_alarm():
    global alarm_thread, stop_event, snooze_event
    time_label.config(fg="red")

    stop_event = threading.Event()
    snooze_event = threading.Event()

    alarm_win = tk.Toplevel(root)
    alarm_win.title("Alarm")
    alarm_win.attributes("-fullscreen", True)
    alarm_win.attributes("-topmost", True)
    alarm_win.configure(bg="black")

    tk.Label(alarm_win, text="Time's up!", font=("Arial", 40),
             fg="white", bg="black").pack(expand=True)

    def on_dismiss():
        """Dismissボタン: ポップアップを閉じ、30秒待ちをスキップさせる
        (シーケンス自体は続行する仕様)"""
        alarm_win.destroy()
        if snooze_event is not None:
            snooze_event.set()
        print("Dismiss pressed.")

    def auto_close():
        if alarm_win.winfo_exists():
            alarm_win.destroy()

    root.after(30000, auto_close)

    btn_frame = tk.Frame(alarm_win, bg="black")
    btn_frame.pack(pady=40)
    tk.Button(btn_frame, text="Dismiss", command=on_dismiss,
              bg="orange", fg="black", font=("Arial", 25),
              padx=30, pady=15).pack(side=tk.LEFT, padx=20)

    def on_sequence_finish():
        root.after(0, lambda: time_label.config(fg="white"))

    alarm_thread = threading.Thread(
        target=alarm_sequence,
        args=(stop_event, snooze_event, on_sequence_finish),
        daemon=True,
    )
    alarm_thread.start()


def show_setting():
    clock_frame.pack_forget()
    setting_frame.pack(fill="both", expand=True)


def show_clock():
    setting_frame.pack_forget()
    clock_frame.pack(fill="both", expand=True)


# =====================================================================
#  ウィンドウ・ウィジェット
# =====================================================================
root = tk.Tk()
root.title("Alarm Clock")
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

clock_frame = tk.Frame(root, bg="black")

time_label = tk.Label(clock_frame, font=("Arial", 80), fg="white", bg="black")
time_label.pack(expand=True)

btn_setup = tk.Button(clock_frame, text="set alerm time", command=show_setting,
                      bg="#333", fg="white", font=("Arial", 15), padx=20, pady=10)
btn_setup.pack(pady=20)

clock_frame.pack(fill="both", expand=True)

setting_frame = tk.Frame(root, bg="black")

tk.Label(setting_frame, text="set alerm time", font=("Arial", 20),
         fg="white", bg="#333").pack(pady=20)

spin_container = tk.Frame(setting_frame, bg="white")
spin_container.pack(expand=True)

hour_spin = tk.Spinbox(spin_container, from_=0, to=23, width=3,
                       font=("Arial", 50), format="%02.0f")
hour_spin.pack(side=tk.LEFT, padx=10)

tk.Label(spin_container, text=":", font=("Arial", 50),
         fg="white", bg="black").pack(side=tk.LEFT)

min_spin = tk.Spinbox(spin_container, from_=0, to=59, width=3,
                      font=("Arial", 50), format="%02.0f")
min_spin.pack(side=tk.LEFT, padx=10)

btn_done = tk.Button(setting_frame, text="set and back to clock", command=show_clock,
                     bg="white", fg="black", font=("Arial", 15), padx=20, pady=10)
btn_done.pack(pady=30)

update_time()
root.mainloop()
