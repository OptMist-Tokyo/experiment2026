from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# 正確なリズムを刻む魔法の工場
factory = PiGPIOFactory()

# ★変更点：最後に「initial_angle=-90」を追加！
# これで「最初は-90度の位置にいるよ」とモーターに教え、無駄なピクつきを防ぎます
servo = AngularServo(
    18, 
    min_angle=-90, 
    max_angle=90, 
    min_pulse_width=0.0005, 
    max_pulse_width=0.0024, 
    initial_angle=0, 
    pin_factory=factory
)

try:
    print("ハンマーを振り上げます（待機状態）...")
    servo.angle = 90 # ※ここはすでにinitial_angleで-90度にいるので、servo.angle = -90 は省略して待つだけにします
    sleep(2)
    for i in range(10):
        print("ピコッ！！（振り下ろす）")
        servo.angle = 0
        sleep(0.3)
        print("ハンマーを元に戻します")
        servo.angle = 90
        sleep(0.3)
except KeyboardInterrupt:
    print("\nプログラムを強制終了しました")

finally:
    servo.detach()
    print("モーターをオフにしました")
