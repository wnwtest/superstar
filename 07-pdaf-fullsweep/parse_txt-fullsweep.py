#-*- coding=utf-8 -*-
import matplotlib.pyplot as plt
from functools import reduce
import sys
import re

def op_main(by_name=u'Sheet1'):
    if len(sys.argv) < 2:
        print("请指定文件路径作为参数")
        return
    
    file_path = sys.argv[1]
    result = extract_data(file_path)
    plot_data(result)
def main():
    op_main()
def extract_data(file_path):
    data = {}
    pattern = re.compile(r"\d{2}-\d{2}\s")  # 匹配日期时间格式如"01-26 "
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if pattern.match(line) and 'lens_pos=' in line:
            parts = line.split(' ')
            lens_pos = None
            pd = None
            defocus = None
            for part in parts:
                if 'lens_pos=' in part:
                    lens_pos = int(part.split('=')[1])
                elif 'pd=' in part:
                    pd = float(part.split('=')[1].strip(','))
                elif 'defocus(um)=' in part:
                    defocus = float(part.split('=')[1].strip(','))

        if lens_pos is not None and pd is not None and defocus is not None:
            data[lens_pos] = {'pd': pd, 'defocus': defocus}
            print(f'lens_pos: {lens_pos}, pd: {pd},defocus: {defocus}')

    # 获取最下面的pd值
    # 按照lens_pos的大小进行排序
    #sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))

    return data
def plot_data(data):
    print("--plot_data--")
    sorted_data = dict(sorted(data.items()))  # 排序数据

    x_values = list(sorted_data.keys())
    pd_values = [v['pd'] for v in sorted_data.values()]
    defocus_values = [v['defocus'] for v in sorted_data.values()]
    print(f'\nlens: {x_values},\npd: {pd_values},\ndefocus: {defocus_values},\n')
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('lens_pos')
    ax1.set_ylabel('pd', color=color)
    ax1.plot(x_values, pd_values, color=color, label='pd')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('defocus', color=color) 
    ax2.plot(x_values, defocus_values, color=color, label='defocus')
    ax2.tick_params(axis='y', labelcolor=color)

    # 添加图例
    fig.legend(loc='upper right')
    
    fig.tight_layout()  
    # 添加网格
    plt.grid(color="k", linestyle=":")
    plt.show()

if __name__ =="__main__":
    main()
