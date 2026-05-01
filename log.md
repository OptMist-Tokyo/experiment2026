# log

2026年度数理情報工学実験の記録です。

## 2026-04-10
##### 投票
大城　🍎
柴垣　🍏
星名　🍓
若林  🍑
西原　🍇


### 案出し
- ゼミの部屋利用管理（大城）🍓
- 指紋からごく短い音楽を生成して流す（柴垣）🍇
- 教室にあるチョークの本数や色の種類を管理する(星名)
- 鍵の開閉状況をwebから見られるようにする(若林)🍇
- エアコンのつけっぱなし防止（大城）
- 代返ちくりシステム（大城）🍏
- 温度センサーで空調自動調節(西原)
- プロジェクターのスクリーンをPCで操作する(若林)🍇
- おすすめの散歩ルートを提案(星名)🍎
- 部屋が暗くなってきたらライトをつける（柴垣）🍑
- スイッチに何か取り付けて照明自動点灯，消灯(西原)
- 会話を聞いて口癖などを分析する(星名)🍑
- 本棚から本を取ってくる(若林)
- しおりがわりにどこまで本を読んだか覚えてくれる（柴垣）
- 歩く速度を計測して教室間の移動に何分かかるかリアルタイムで予測(星名)🍇
- 信号の待ち時間を可視化(若林)
- カーナビの指示に合わせて顔/指の向きが変わるロボット(若林)
- どの部屋に何人人がいるのか管理（大城）🍑🍓
- 学食メニュールーレット（大城）🍏
- 落としてみてかかる時間で高さ計測(若林)🍇
- 大谷がヒットを打つと口調の機嫌が良くなる（柴垣）
- ちゃんと起きたか判断してスヌーズする目覚まし時計(若林)🍓🍎
- 授業中の映像を分析して寝ている確率を表示(星名)　🍎
- 手書き数式の画像を読み込んで字のきれいさを評価(若林)🍏🍎
- 筋トレの負荷計測して「あと一回」とか言ってくるトレーナー（大城）🍏
- 圧力センサーで寝返り計測(西原)
- 弱いと舐めてくるパンチングマシーン（柴垣）🍑
- 乗り換え前に教えてくれる(若林)
- 雨の日の地面を「水溜りをギリギリで避けるゲーム」に変える(星名)🍑
- 赤信号にひっかかりにくい道を提案(若林)🍓
- 途中まで歌うと続きを再生(若林)🍎
- ものをどこに置いたか覚えておく(若林)🍓
- MMDDが素数の日だけ数学の話してくる(若林)🍏
- どの部屋に何人人がいるのか管理（大城）🍑🍇🍎
- ちゃんと起きたか判断してスヌーズする目覚まし時計(若林) 
- 手書き数式の画像を読み込んで字のきれいさを評価(若林)🍏🍓

### やったこと

- 目標決め
- 必要物品洗い出し

### 決まったこと

- ~~6号館2階の各部屋に何人（誰がかも）いるか外部から見られるものを作る~~→2017とだだかぶり
- ちゃんと起きたか判断してスヌーズする目覚まし時計を作る
  
##### 追加機能の案

- ~~キリ番をお祝い~~
- ~~上にカメラ付けてどこら辺が空いてるか管理~~
- ~~人口密度をディスプレイの色で可視化~~
  
- 本当にやばい時間になったら叩き起こす
- あと何回で殴るぞと脅す
- 寝坊をチクる
- 照明と連動
- スケジュールを組めるようにする
  
##### 必要なもの

- 圧力センサ　（購入）
- サーボモーター（あった）
- スイッチモジュール　　
- ピコピコハンマー　（購入）
 
- バイブレーター（小型モーターで良さそう）
- スピーカー　（あるかも）
- ボタン　（購入）
- 液晶　（購入）
- ケーブル類（購入）

### ToDo・役割決め

- 時計機能（ボタンでの操作・時刻表示・タイマー）　（星名・若林）
- モーター制御　（大城・柴垣）
- 圧力センサでの起床検知（西原）
  


## 2026-04-17

### 購入物品決め＆各チーム作業

#### 買うもの
- [トランジスタ  S8550](https://www.amazon.co.jp/Chanzon-%E3%83%90%E3%82%A4%E3%83%9D%E3%83%BC%E3%83%A9%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B8%E3%82%B9%E3%82%BF-100%E5%80%8B-S8550-TO-92PNP%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B8%E3%82%B9%E3%82%BF-0-5A/dp/B08M3YHQ57)
- [圧力センサ  FSR406](https://www.amazon.co.jp/uxcell-%E8%96%84%E8%86%9C%E5%9C%A7%E5%8A%9B%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC-20g-10Kg-%E3%83%95%E3%82%A9%E3%83%BC%E3%82%B9%E3%82%BB%E3%83%B3%E3%82%B7%E3%83%B3%E3%82%B0%E6%8A%B5%E6%8A%97%E5%99%A8-%E3%82%B9%E3%83%88%E3%83%AC%E3%82%B9%E3%83%86%E3%82%B9%E3%83%88%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E3%83%91%E3%83%83%E3%83%89/dp/B0F5HDRYRH)
- [ADコンバータ  MCP3008-I/P](https://www.amazon.co.jp/PENGLIN-MCP3008-I-MCP3008-8%E3%83%81%E3%83%A3%E3%83%8D%E3%83%AB10%E3%83%93%E3%83%83%E3%83%88A-D%E3%82%B3%E3%83%B3%E3%83%90%E3%83%BC%E3%82%BF%E3%80%81SPI%E3%82%B7%E3%83%AA%E3%82%A2%E3%83%AB%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%95%E3%82%A7%E3%82%A4%E3%82%B92-7V%E3%80%81DIP-16%E4%BB%98%E3%81%8D/dp/B0G5YJSQTC/ref=sr_1_5?dib=eyJ2IjoiMSJ9.esSxHu-2wIj7QCTsof-X0SJlYnD1HDNEKbGDEEUQsLKTBvz3R9EG3y8nA705ogNsayqkngMYCQ26dY1JZzUAvJvv1M0feN-Qy7Dh8RnsT2BjxggaDDCSUrTTe57mpYS1cbWP9YwPjSE9lnybC-mo4F3Vi6dC7wuekAgsoi8Ghk2gWUr0mVBvfETLj8NqQWCEr444jkxh1N2yPctjCw0if5GGX-Eey3Dm9q5XXddNA_70ipqAacYhRomtqioasALGC7kBmh85ucmeJWFhJoGJQ5qOdt8pF-N2ZIAzyYqaByk.jGi4gVKcJHF5YNMJ_saEmi77Pff99E3jC1uP_P6RCz4&dib_tag=se&keywords=mcp3008&qid=1776410247&sr=8-5)
- [ディスプレイ](https://www.amazon.co.jp/OSOYOO-3-5%E3%82%A4%E3%83%B3%E3%83%81LCD%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4-%E3%82%BF%E3%83%83%E3%83%81%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3-Raspberry-Model/dp/B01N5HW3BP?th=1)
- [ピコピコハンマー](https://www.amazon.co.jp/%E3%83%8F%E3%83%B3%E3%83%9E%E3%83%BC%E3%83%91%E3%83%B3%E3%83%81-%E3%81%9F%E3%81%9F%E3%81%8F%E3%81%A8%E3%83%94%E3%82%B3%E3%83%94%E3%82%B3%E9%9F%B3%E3%81%8C%E9%B3%B4%E3%82%8B%E3%83%94%E3%82%B3%E3%83%94%E3%82%B3%E3%83%8F%E3%83%B3%E3%83%9E%E3%83%BC%E3%81%A7%E3%81%99-%E3%81%8A%E4%BB%95%E7%BD%AE%E3%81%8D-%E3%83%91%E3%83%BC%E3%83%86%E3%82%A3%E3%83%BC-%E7%9B%9B%E3%82%8A%E4%B8%8A%E3%81%8C%E3%82%8B%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E3%81%A7%E3%81%99/dp/B0DWRYYY71/ref=sr_1_9?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2J582P73O6BCV&dib=eyJ2IjoiMSJ9.uNbosAR-uOWJ27R1HXB6FTOh6DeuMcXdhnIsLiS10BW52ca5IE7u5POkOvaFT5sCEegZ7bGNMn9UL0piVy-OEUwd4krQWJXb4eU4nOdrBlLjC1VubkFWS8RYXVlGR4nqQWfgdJj7aNgyAAHVJEqoAXxyeJKdWHxaW1V1u53bMPH_RSs3SMMHSiwKMUGUhqNU67u90YqgzGjo8kjbaJgQFLfDQu5M2TFQnfE-zCRH6V1TjzAu56R8U-CtfP8W4y1nfYm9b4UteNmpBKhZ_THZix_xVypnoCaWEIpxIAbY9WY.53KGX8YJqGroXvbkpCzeeWGQyvJ9XYmGawxWIMxZ45k&dib_tag=se&keywords=%E3%83%94%E3%82%B3%E3%83%94%E3%82%B3%E3%83%8F%E3%83%B3%E3%83%9E%E3%83%BC&qid=1776410029&sprefix=%E3%83%94%E3%82%B3%E3%83%94%E3%82%B3%E3%83%8F%E3%83%B3%E3%83%9E%E3%83%BC%2Caps%2C205&sr=8-9)
次回以降購入かも
- [クランプ](https://www.amazon.co.jp/%E9%AB%98%E5%84%80-TAKAGI-%E5%BC%B7%E5%8A%9B%E5%9E%8B-C%E3%82%AF%E3%83%A9%E3%83%B3%E3%83%97-100mm/dp/B006JZI80E/ref=sr_1_3?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2GXUMG859R0P7&dib=eyJ2IjoiMSJ9.dONHMEwtmXKKmHuuprlyleGcRr1o1ricb8-3p6d9BumFyf8KRNGXSg4WNEDydUqZI3z2LEg2ZWwb6uL8b92Bgp3FfuNMwGmvtjrz9LOQiJzpBgu9EHmjL6W9-MR7iT0Vt4FGwYoBhiuDaImDu4rRpuH547xfDcj69IvntgspxkiSAxfAOp_xYrFrshMMB2j2Y_qhIMcPz65Io9HmHHMJGWOKEfadQZDVrj7rxSY51S5hDGmfEAxm6FC5A4Wn1wmTIhTjqKBTv_QAJie_kzkFSsyC2AoPmqFweuB43CZ2KEk.KV8z_yPMseRBgha_oqYh9BiT2QzBkFjrhHxmlAiNTAc&dib_tag=se&keywords=%E9%AB%98%E5%84%80%2B%E3%82%B7%E3%83%A3%E3%82%B3%E4%B8%87%E5%8A%9B&qid=1777611491&s=diy&sprefix=%E9%AB%98%E5%84%80%E5%BC%8F%2B%E3%82%B7%E3%83%A3%E3%82%B3%E4%B8%87%E5%8A%9B%2Cdiy%2C147&sr=1-3&th=1)
- 木材
- サーボブラケット

#### やったこと
- 時計機能のコーディング
- サーボモータの動作チェック
- サーボモータ制御のコーディング
- 購入物品洗い出し

#### Todo
届いたもの使ってハードウェアをできるところまで作ります


## 2026-04-24
### チームごとに作業

### やったこと
ピコハン
- ガムテープでサーボモーターに固定
- 液晶が邪魔でピンから信号取れない問題→ジャンパ線を曲げられるように加工

時計
- LCDの動作チェック

圧力センサ
- ADコンバータと繋いで出力を確認


### ToDo

- 圧力センサの出力の調整
- サーボの固定
- 箱作り
- ブザーの回路組む
- 諸々の連携

## 2026-05-01
### チームごとに作業

### やったこと
- 前回の最後に起動しなくなったraspberry piを直した
- サーボモータと圧力センサのブレッドボードを一つに統合
- 圧力センサの動作確認
- 液晶、圧力センサ、サーボモータを同時に接続できるようにした

### 残りのTodo

- 電子ブザーを動くようにする
- ピコハンのクランプによる固定
- 圧力センサの閾値判定
- スヌーズ機能
- ３つの機能をソフトウェアとして統合
  - 時計をメインとしつつ他の機能を関数として呼び出せばできそう
- 見た目をもう少し整えましょう

