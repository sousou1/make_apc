import math

input_width = 16
au = 2
nowlayer = 1
exp2 = 0
write_str = ""
width = []
normal_width = []
rem = []

print("input bit幅" + str(input_width) + " AU層" + str(au))

if au > (math.floor(math.log2(input_width)) - 1):
	au = (math.floor(math.log2(input_width)) - 1)


def all_under_2(lst):
	for num in lst:
		if num>2:
			return False
	return True

def add_reg_string_num(num):
	if num == 0:
		return ""
	else:
		return "[" + str(num) + ":0]"


# AU層を決定する
# widthは各段の桁上げの数
# remはあまり
width.append(input_width)
rem.append(0)

if math.log2(input_width) == int(math.log2(input_width)):
	while nowlayer <= au:
		width.append(math.floor(width[nowlayer - 1] / 2))
		rem.append(0)
		exp2 += 1
		nowlayer += 1
else:
	while nowlayer <= au:
		plus = 0
		# au層の最後でremの加算結果をwidthに移動
		if nowlayer == au:
			plus = 1
		width.append(math.floor(width[nowlayer - 1] / 4) * 2 + plus)
		rem.append(nowlayer + 1 - plus)
		nowlayer += 1

# remを除いたau層後の最終的なビット幅
# まず、一番下の桁の加算器の数を計算
# 15個なら4個の桁上げ加算器、5個の一桁上の数、5個の同じ桁の数が出力される
# normal_widthに[5, 5]を追加
# 次, 1桁目4を3で割った数の1+あまりの2=3が一番下、2桁目桁上げ1 + 4を3で割った数の1+あまりの1=3が2桁目, 3桁目は桁上げの1
# つまり[3, 3, 1]を追加
# 次、[1, 2, 2]
# 全部2以下になれば桁上げ加算
# [1, 1, 1, 1]

# log2を取り、桁数を計算、その桁数以上になることはないので、幅を調整
# width3個ずつ加算、2個余ったらpc_remで加算

while 1:
	temp = []
	i = 0
	carry = 0
	if isinstance(width[nowlayer - 1], list):
		for num in width[nowlayer - 1]:
			temp.append(num // 3 + carry + num % 3)
			carry = num // 3
		# 一番上位bitのcarry
		if carry > 0:
			temp.append(carry)
	# listでなければ最初の一回目なので
	else:
		temp.append(width[nowlayer - 1] // 3 + width[nowlayer - 1] % 3)
		if width[nowlayer - 1] // 3 > 0:
			temp.append(width[nowlayer - 1] // 3)

	# 各桁何bitあるかを計算
	width.append(temp)
	rem.append(rem[nowlayer - 1])
	nowlayer += 1
	if all_under_2(temp):
		break

# 最終的な桁数を保存
sum_dig = rem[nowlayer - 1]
for num in width[nowlayer - 1]:
	sum_dig += 1

# 最終的な段数を保存し、nowlayerをリセット
sum_layer = nowlayer - 1
nowlayer = 1


write_str += "module APC(\n"
write_str += "\tinput wire clk,\n"
write_str += "\tinput wire " + add_reg_string_num(width[0] - 1) +" in,\n"
write_str += "\toutput reg"+ add_reg_string_num(sum_dig) +" sum,\n"
write_str += "\toutput reg exp2\n"
write_str += ");\n"


print("-----debug : 各層の桁数、あまり、exp2----")
print(width)
print(rem)
print("exp2=" + str(exp2))
print("-------")
while nowlayer <= au:
	write_str += "\treg "+ add_reg_string_num(width[nowlayer] - 1) + " au" + str(nowlayer) + ";\n"
	if(rem[nowlayer] > 0):
		write_str += "\treg "+ add_reg_string_num(rem[nowlayer] - 1) + " rem" + str(nowlayer) + ";\n"
	nowlayer += 1

while nowlayer <= sum_layer:
	i = 0
	if isinstance(width[nowlayer], list):
		for dig in width[nowlayer]:
			write_str += "\treg "+ add_reg_string_num(dig - 1) + " pc" + str(nowlayer) + "_" + str(i) + ";\n"
			i += 1
	else:
		write_str += "\treg ["+ add_reg_string_num(width[nowlayer] - 1) + " pc" + str(nowlayer) + "_" + str(i) + ";\n"
	if(rem[nowlayer] > 0):
		write_str += "\treg "+ add_reg_string_num(rem[nowlayer] - 1) + " rem" + str(nowlayer) + ";\n"
	nowlayer += 1

# nowlayerリセット
nowlayer = 0


write_str += "\talways @(posedge clk) begin\n"
while nowlayer < sum_layer:
	nowlayer += 1
	# AU層
	if nowlayer <= au:
		# 最初の一段の場合、入力はwidthではなくin
		if nowlayer == 1:
			write_str += "\t\tfor (int i=0; i<" + str(int(width[nowlayer]/2)) + "; i += 1) au" + str(nowlayer) + "[i] <= in[i] && in[i+1];\n"
			write_str += "\t\tfor (int i=" + str(int(width[nowlayer]/2)) + "; i<" + str(width[nowlayer]) +"; i += 1) au" + str(nowlayer) + "[i] <= in[i] || in[i+1];\n"
			# remが存在する場合、通常の加算であまりを計算する
			if rem[nowlayer] > 0:
				# n桁以下は伝播させる
				write_str += "\t\trem" + str(nowlayer) + "<= in" + str(width[nowlayer] + 1)
				temp = rem[nowlayer] - nowlayer - 1
				while temp != 0:
					write_str += "+in[" +  str(width[nowlayer] + rem[nowlayer] - temp) + "]"
					temp += 1
				write_str +=";\n"

		else:
			if (nowlayer % 2) == 0:
				write_str += "\t\tfor (int i=0; i<" + str(int(width[nowlayer]/2)) + "; i += 1) au" + str(nowlayer) + "[i] <= au" + str(nowlayer - 1) + "[i] && au" + str(nowlayer - 1) + "[i+1];\n"
				write_str += "\t\tfor (int i=" + str(int(width[nowlayer]/2)) + "; i<" + str(width[nowlayer]) +"; i += 1) au" + str(nowlayer) + "[i] <= au" + str(nowlayer) + "[i] || au" + str(nowlayer) + "[i+1];\n"
			else:
				write_str += "\t\tfor (int i=0; i<" + str(int(width[nowlayer]/2)) + "; i += 1) au" + str(nowlayer) + "[i] <= au" + str(nowlayer - 1) + "[i] || " + str(nowlayer - 1) + "[i+1];\n"
				write_str += "\t\tfor (int i=" + str(int(width[nowlayer]/2)) + "; i<" + str(width[nowlayer]) +"; i += 1) au" + str(nowlayer) + "[i] <= au" + str(nowlayer) + "[i] && au" + str(nowlayer) + "[i+1];\n"
			if rem[nowlayer] > 0:
				write_str += "\t\trem" + str(nowlayer) + "<= in" + str(width[nowlayer] + 1)
				temp = rem[nowlayer] - 1
				while temp != 0:
					write_str += "+au" + str(nowlayer) + "[" + str(width[nowlayer] + rem[nowlayer] - temp) + "]"
					temp -= 1
				write_str +=";\n"

	# 普通の並列加算器の生成
else:
	if nowlayer == 1:
		if isinstance(width[nowlayer], list):
			t = 0
			for dig in width[nowlayer]:
				write_str += "\t\tfor (int i=0; i<" + str(dig)  + "; i += 1) pc" + str(nowlayer) + "_" + str(t) + "[i] <= in[i] && in[i+1];\n"
				t += 1
	else:
		if isinstance(width[nowlayer], list):
			t = 0
			for dig in width[nowlayer]:
				if dig == 1:
					write_str += "\t\tpc" + str(nowlayer) + "_" + str(t) + " <= in[i] && in[i+1];\n"

				write_str += "\t\tfor (int i=0; i<" + str(dig)  + "; i += 1) pc" + str(nowlayer) + "_" + str(t) + "[i] <= in[i] && in[i+1];\n"
				t += 1
		if rem[nowlayer] > 0:
			write_str += "\t\trem" + str(nowlayer) + "<= in" + str(width[nowlayer] + 1)
			temp = rem[nowlayer] - 1
			while temp != 0:
				write_str += "+au" + str(nowlayer) + "[" + str(width[nowlayer] + rem[nowlayer] - temp) + "]"
				temp -= 1
			write_str +=";\n"

write_str += "\tend\n"
write_str += "endmodule\n"

print(write_str)
			





'''以下PC層
sum3 =  math.ceil(11/3)
rem3 =  au 
out_width = math.floor(math.log2(x)) + 1



4 < math.log2(18) < math.log2(x)
18 
4and  4or  2bit桁上げ  8
4 4 1  | 1  10r
2or 2and   4
1 1 | 1 | 1 4r

module APC(
	input wire clk,
	input wire [$width - 1:0] in,
	output[$W:0] out
);

logic [($width1+$rem1 - 1):0] sum1;
logic [($width2+$rem2 - 1):0] sum2;



always_ff @(posege clk) begin
	for (int i=0; i<$width / 2; i += 1) sum1[i] <= in[i*2+0] & in[i*2+ 1];
	for(int i = $width / 2 ; i < $width ; i += 1) sum1[i] <= in[i*2+0] | in[i*2+ 1];
	sum1[$width:$width+1] = in[$width*2] + in[&width*2+1];

—以下PC層—
	for(int
	




reg AND1_1, AND1_2, ….. AND1_($width1 / 2), ~OR1_($width1 / 2), (if rem1)REM1_1,
reg OR2_1, ~ OR2_($width2/ 2), ~AND2_$width2, REM2_2, (if rem1)REM2_1

 always @(posedge clock) begin
	AND1_1 <= input[0] & input[1];
	AND1_2 <= 
…
	REM1_1 <= input[width - 1] 

	OR2_1 <= AND1_1 | AND1_2
	AND2_1 <= OR1_1 | OR1_2
	REM2_1 <= REM1_!
wire 

assign output[0] = REM$au_0
assign output[1] = REM$a

assign AND1_1
~
assign AND1_($width1/2)
assign OR1_($width1/2 + 1)
~
assign OR1_$width

assign OR2_1
~
assign OR2_($width2/4)

assign

'''