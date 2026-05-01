import spidev
import time

# SPI通信のセットアップ
spi = spidev.SpiDev()
spi.open(0, 0)             # バス0, CS0 (CE0: 24番ピン) を使用
spi.max_speed_hz = 1350000 # 通信速度の設定

def read_adc(channel):
    """MCP3008から指定したチャンネル(0〜7)のアナログ値を読み取る"""
    if channel < 0 or channel > 7:
        return -1
    
    # MCP3008に送る3バイトのコマンドを作成
    # 1バイト目: スタートビット(1)
    # 2バイト目: シングルエンドモード(1) + チャンネル番号
    # 3バイト目: ダミーデータ(0)
    command = [1, (8 + channel) << 4, 0]
    
    # SPIでデータを送受信
    adc = spi.xfer2(command)
    
    # 受信した3バイトのデータから、10ビットの測定値を抽出
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    print("=== 圧力センサーのテストを開始します ===")
    print("センサーを指で押してみてください。(Ctrl+Cで終了)")
    print("-" * 40)
    
    while True:
        # CH0 (MCP3008の1番ピン) の値を読み取る
        value = read_adc(0)
        
        # 視覚的にわかりやすいようにバー（#）を表示
        bar = "#" * int(value / 25)
        
        # 値(0〜1023)とバーを画面に出力（★古いPythonでも動く書き方に修正済み）
        print("圧力値: {:4d} | {}".format(value, bar))
        
        # 0.1秒待機
        time.sleep(0.1)

except KeyboardInterrupt:
    # Ctrl+Cが押された時の処理
    print("\nテストを終了します。")

finally:
    # 最後にSPI通信を閉じる
    spi.close()
