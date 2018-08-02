# make_apc

ストカスティック演算に用いるAPC(https://ieeexplore.ieee.org/document/540843/)
のシミュレーターおよびVelilogHDL作成ツール
## apc.py
APCのシミュレータ

apc.pyの使用方法
layer:AU層の数
bit_width：入力のbit幅
diftimes：シミュレーション回数
を入力することで、diftimesを回した後、差が何回出たかが表示される。
出力例
-4〜5
[0, 0, 76, 240, 339, 271, 74, 0, 0, 0]

## make_apc.py
APCのVerilogHDLを作成するツール
input_width：入力のbit幅
au：au層
を入力することで、APCを実装するためのVelilogHDLを出力する。