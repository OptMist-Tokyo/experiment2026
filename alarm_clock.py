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
# --- ブザー（GPIO17） ---
buzzer = PWMOutputDevice(17)

# --- サーボ／ハンマー（GPIO18, pigpio経由） ---
# 注意: 事前に `sudo pigpiod` でデーモンを起動しておくこと
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

# --- 圧力センサー電源（GPIO26）＋ SPI（バス1/CS2, ch0） ---
sensor_power = OutputDevice(26)
sensor_power.on()

spi = spidev.SpiDev()
spi.open(1, 2)
spi.max_speed_hz = 1350000


def cleanup():
    """終了時にすべてのデバイスを安全に止める"""
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
    """「ピピッ×10回」を1サイクル鳴らす。stop_event が立ったら即中断。"""
    for _ in range(10):
        for _ in range(2):
            if stop_event.is_set():
                stop_tone()
                return
            play_tone(3200, 0.5)
            sleep(0.1)
            stop_tone()
            sleep(0.05)
        for _ in range(12):  # 0.6秒の無音を細かく刻む
            if stop_event.is_set():
                return
            sleep(0.05)


def buzz_loop(stop_event):
    """stop_event が立つまでブザーを鳴らし続ける"""
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
    """
    一定時間センサーを監視し、起きているか（ベッドから離れているか）を判定する。
    半分以上の測定でしきい値を下回れば「起きた」とみなす。
    """
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
    """ハンマーを指定回数振り下ろす。stop_event が立ったら即中断。"""
    servo.angle = 90  # 振り上げ（待機位置）
    sleep(0.5)
    for i in range(times):
        if stop_event.is_set():
            break
        print("ピコッ！！（振り下ろす） {}/{}".format(i + 1, times))
        servo.angle = 0
        sleep(0.3)
        servo.angle = 90
        sleep(0.3)
    servo.angle = 0  # 中立位置へ戻す


# =====================================================================
#  アラームシーケンス（フローチャート通り）
#
#  [アラーム時刻]
#      ↓
#  [圧力チェック] → 起きていたら → [停止]
#      ↓ 寝ている
#  [ブザーON] ←─────────────────────────────────────┐
#      ↓                                              │
#  [30秒待つ or スヌーズで早送り]                      │
#      ↓ どちらでも同じ流れへ                          │
#  [ブザーOFF → 1分待機]                              │
#      ↓                                              │
#  [圧力チェック] → 起きていたら → [停止]              │
#      ↓ 寝ている                                     │
#  [ブザー＋ハンマー(30回)]                            │
#      └──────────────────────────────────────────────┘
# =====================================================================
stop_event = None
snooze_event = None
alarm_thread = None


def alarm_sequence(stop_ev, snooze_ev, on_finish):
    """
    フローチャートに沿ったアラームシーケンス。別スレッドで実行。
    stop_ev  : Dismiss または起床確認でセット → 全停止
    snooze_ev: スヌーズボタンでセット → 30秒待ちを即座にスキップ
    on_finish: シーケンス終了時のGUIコールバック
    """
    try:
        # ── ステップ1: 最初の圧力チェック ──────────────────────────
        if is_awake():
            print("✅ すでに起きています。アラーム停止。")
            stop_ev.set()
            return

        # ── メインループ ─────────────────────────────────────────
        while not stop_ev.is_set():

            # ── ステップ2: ブザーON ──────────────────────────────
            buzz_stop = threading.Event()
            buzz_thread = threading.Thread(
                target=buzz_loop, args=(buzz_stop,), daemon=True
            )
            buzz_thread.start()
            print("🔔 ブザーON")

            # ── ステップ3: 30秒待つ（スヌーズで早送り可） ───────────
            snooze_ev.clear()
            wait_start = time()
            while time() - wait_start < 30:
                if stop_ev.is_set():
                    break
                if snooze_ev.is_set():
                    print("💤 スヌーズ押下: 30秒待ちをスキップ")
                    break
                sleep(0.1)

            if stop_ev.is_set():
                buzz_stop.set()
                buzz_thread.join(timeout=3)
                break

            # ── ステップ4: ブザーOFF → 1分待機 ──────────────────
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

            # ── ステップ5: 圧力チェック ──────────────────────────
            if is_awake():
                print("✅ 起床確認。停止。")
                stop_ev.set()
                break

            # ── ステップ6: ブザー＋ハンマー(30回) ───────────────
            print("⏰ まだ寝ています。ブザー＋ハンマー開始。")
            buzz_stop = threading.Event()
            buzz_thread = threading.Thread(
                target=buzz_loop, args=(buzz_stop,), daemon=True
            )
            buzz_thread.start()

            hammer_strike(30, stop_ev)

            buzz_stop.set()
            buzz_thread.join(timeout=3)

            # ループ先頭（ステップ2: ブザーON）へ戻る

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
last_fired_minute = None  # 同じ分で二重発火を防ぐ


def update_time():
    global last_fired_minute
    now = datetime.now()
    time_label.config(text=now.strftime("%H:%M:%S"))

    alarm_h = hour_spin.get().zfill(2)
    alarm_m = min_spin.get().zfill(2)
    current_minute = now.strftime("%H:%M")
    alarm_minute   = "{}:{}".format(alarm_h, alarm_m)

    # 「秒==0」の一致待ちをやめ、分が一致した瞬間に即発火。
    # 同じ分で二重発火しないよう last_fired_minute で管理。
    if (current_minute == alarm_minute
            and current_minute != last_fired_minute
            and (alarm_thread is None or not alarm_thread.is_alive())):
        last_fired_minute = current_minute
        trigger_alarm()

    # 200msごとにポーリングして発火タイミングを取りこぼさない
    root.after(200, update_time)


def trigger_alarm():
    global alarm_thread, stop_event, snooze_event
    time_label.config(fg="red")

    stop_event = threading.Event()
    snooze_event = threading.Event()

    # ── アラームポップアップ ──────────────────────────────────────
    alarm_win = tk.Toplevel(root)
    alarm_win.title("Alarm")
    alarm_win.attributes("-fullscreen", True)
    alarm_win.attributes("-topmost", True)
    alarm_win.configure(bg="black")

    tk.Label(alarm_win, text="Time's up!", font=("Arial", 40),
             fg="white", bg="black").pack(expand=True)

    def on_snooze():
        """スヌーズ: ポップアップを閉じ、30秒待ちをスキップさせる"""
        alarm_win.destroy()
        if snooze_event is not None:
            snooze_event.set()
        print("Snooze pressed.")

    def on_dismiss():
        """Dismiss: 全停止"""
        alarm_win.destroy()
        if stop_event is not None:
            stop_event.set()
        time_label.config(fg="white")
        print("Alarm dismissed.")

    btn_frame = tk.Frame(alarm_win, bg="black")
    btn_frame.pack(pady=40)
    tk.Button(btn_frame, text="Snooze", command=on_snooze,
              bg="orange", fg="black", font=("Arial", 25),
              padx=30, pady=15).pack(side=tk.LEFT, padx=20)
    tk.Button(btn_frame, text="Dismiss", command=on_dismiss,
              bg="#555", fg="white", font=("Arial", 25),
              padx=30, pady=15).pack(side=tk.LEFT, padx=20)

    def on_sequence_finish():
        root.after(0, lambda: time_label.config(fg="white"))

    alarm_thread = threading.Thread(
        target=alarm_sequence,
        args=(stop_event, snooze_event, on_sequence_finish),
        daemon=True,
    )
    alarm_thread.start()


# ── 画面切り替え ──────────────────────────────────────────────────
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

# ── 1. 時計画面 ───────────────────────────────────────────────────
clock_frame = tk.Frame(root, bg="black")

time_label = tk.Label(clock_frame, font=("Arial", 80), fg="white", bg="black")
time_label.pack(expand=True)

btn_setup = tk.Button(clock_frame, text="set alerm time", command=show_setting,
                      bg="#333", fg="white", font=("Arial", 15), padx=20, pady=10)
btn_setup.pack(pady=20)

clock_frame.pack(fill="both", expand=True)

# ── 2. 設定画面 ───────────────────────────────────────────────────
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

# =====================================================================
#  実行
# =====================================================================
update_time()
root.mainloop()
