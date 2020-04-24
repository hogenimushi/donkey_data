# donkeycarのデータをいろいろ加工するやつ
必ずtubのバックアップを行なってからスクリプトを実行する様にしてください  

## データの周波数を変えるやつ
$ python3 change_freq.py --current "current freq" --target "target freq" --input "file path" --output "file_path" --test

オプション  
--current データを取得するときに使用した周波数を入力してください(default=20)  
--target　作りたいデータの周波数を入力してください(default=10)  
--input　データのpathを入力してください  
--output データの保存先を入力してください
--test　付近のデータを読み込んで近似してみるモード（少しは滑らかになるかも？）  
  
example  
$ python3 change_freq.py --input tub_19_20-04-20 --test --output aaa 
  
この例の場合、  
aaa_0、aaa_1の二つのディレクトリにデータができます
## データから特定の部分だけ抜き出すやつ
$ python3 trimming_data.py "data path" "first record number" "last record number" "destination data path"  
  
data pathに現在の学習データのディレクトリを、  
first record numberに切り取りたいデータの範囲の最初の番号を、  
last record numberに切り取りたいデータの範囲の最後の番号を、  
destination data pathに保存先のディレクトリを入力してください。
## データから特定の部分をまとめて抜き出すやつ
$ python3 trimming.py --input "data directory" --output "destination directory" --file "file" --num "data list"   
  
fileの例  
40 50  
600 700  
  
コマンドの例
$ python3 trimming_from_file.py --input /Users/iori/tmp/virtual_race_data/mod_lap10/ --output /Users/iori/tmp/virtual_race_data/ccc --num 40 50 600 700  
  
この例の場合,  
aaa_0ディレクトリに40-50、
aaa_1ディレクトリに600-700が保存されます 
## おまけ
plot.ipynbでjsonを読んで中身をプロットできる(未整備)
