from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()

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
    servo.angle = 90 
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
