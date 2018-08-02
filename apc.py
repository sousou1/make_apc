import random
import math

layer = 1 # AU層の数
bit_width = 9 # bit幅
diftimes = 1000 # 何回AU層ありとなしの差を計測するか

'''
bitlist例
bitlist = [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1]


ランダムbitlist作成
p = 0
while p < bit_width:
	bitlist.append(random.randint(0, 1))
	p += 1
print(bitlist)
'''

# 入力のi番目とi+1番目の演算結果を(i / 2)番目の一時的なリストに格納
def bit_and(inbit, outbit, i):
	outbit.append(inbit[i] and inbit[i + 1])

def bit_or(inbit, outbit, i):
	outbit.append(inbit[i] or inbit[i + 1])

# 何層目の上から何番目かを指定することでandかorかを決定
def bit_cal(inbit, outbit, i, nowlayer, bit_width):
	# 奇数層かつ下半分, もしくは偶数層かつ上半分ならor, それ以外ならand
	if (nowlayer + (i < bit_width / 2)) % 2:
		bit_or(inbit, outbit, i)
	else:
		bit_and(inbit, outbit, i)

# bit列, AU層の数, bit列の長さを渡し, AU層を通した後, 合計した値を返す
def apc(bitlist, layer, bit_width):
	nowlayer = 0 # 処理したAU層の数
	result = 0 # AU層で処理した後の合計
	templist = [] # 計算結果を入れるリスト
	middlelist = [] # 層の計算を行うごとにtemplistで更新

	# 一層目の計算のために元となるビット列の読み込み
	middlelist = bitlist
	# AU層にlayerで回数通す
	while nowlayer < layer:
		nowlayer  += 1
		i = 0;
		while i + 1 < bit_width:
			bit_cal(middlelist, templist, i, nowlayer, bit_width)
			i += 2
		if i < bit_width:
			# あぶれたビット列の計算（元のbit列が2のべき乗の場合必要なし）
			result += middlelist[i] * nowlayer

		# 層の計算が全て終わった後、middlelistにtemplistを代入しtemplistをクリア
		middlelist = templist 
		templist = []
		# ビット幅を半分に
		bit_width = int(bit_width / 2)
		# print(middlelist)

	# 最後のAU層が終わった後、結果を計算
	for bit in middlelist:
		result += bit * (2 ** layer)
	return result


times = 0
dif = 0
diflst = [0] * (bit_width + 1) # 差を計測する際に利用

while times < diftimes: # diftimesだけ繰り返す
	bitlist = []
	p = 0
	while p < bit_width: # ランダムbit列作成
		bitlist.append(random.randint(0, 1))
		p += 1
	result = apc(bitlist, layer, bit_width)

	# 正確な演算と比較
	acculate_result = 0
	for bit in bitlist:
		acculate_result += bit
	dif = result - acculate_result + math.ceil(bit_width / 2)

	diflst[dif] += 1

	times += 1

print("-" + str(int(bit_width / 2)) + "〜" + str(math.ceil(bit_width / 2)))
print(diflst)
