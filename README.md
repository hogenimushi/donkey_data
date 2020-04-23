# donkey_data
Datasets for Donkeycar training

# 使い方
1. どんきーいれる
1. myconfig.pyを書き換える．とくに，simulatorのパス
1. Makefileのターゲットを見る．
1. がんばる

# 例

早く走るモデルをつくる
 make train_fast20

作ったモデルで走らせる
 make run_fast20

# やること
- 10Hzに対応する
- スクリプトの整理
- クラッシュしまくるデータを作る -->　リカバーするデータを作る
- コースアウトからリカバーするデータを作る
- 他車を抜く，避けるデータを作る
- 20Hz->10Hz変換器
- 狙ったデータを抜き出すスクリプト


