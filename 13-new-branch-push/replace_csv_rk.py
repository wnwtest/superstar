# -*- coding: utf-8 -*-
import csv

# 读取CSV文件
with open('paths.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)

# 删除每行开头的/Data_8T1/wangnanwang/tools/
for i in range(len(lines)):
    for j in range(len(lines[i])):
        lines[i][j] = lines[i][j].replace("/Data_8T1/wangnanwang/tools/", "", 1)  # 只替换第一个匹配项

# 写入新的CSV文件
with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for line in lines:
        writer.writerow(line)