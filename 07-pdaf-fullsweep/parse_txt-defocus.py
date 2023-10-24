#-*- coding=utf-8 -*-
import matplotlib.pyplot as plt
from functools import reduce
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号


def op_main(by_name=u'Sheet1'):
    file_path = "pdaf_fullsweep_log1011.txt"    
    result = extract_data(file_path)

    '''
    坐标范围
    总结一下，下面形式的函数可以控制图像的绘图范围：
    plt.axis([x_min, x_max, y_min, y_max])
    如果只是单独想要控制x轴或者y轴的取值，则可以用plt.xlim(x_min, x_max)和plt.ylim(y_min, y_max)，用法与plt.axis()类似。
    '''
    x0_min =0
    x0_max=400
    plt.xlim(x0_min, x0_max)
    y0_min =-300
    y0_max=300
    plt.ylim(y0_min, y0_max)
    for lens_pos, pd in result.items():
        print(f'lens_pos: {lens_pos}, defocus: {pd}')
    x = list(result.keys())
    y = list(result.values())
    #plt.yticks(my_y_ticks)
    plt.title("fullsweep defocus")
    plt.xlabel("Lens pos")
    plt.ylabel("defocus Value")
    #plot函数作图
    plt.plot( x,y, color="r",label='defocus')

    # 简单的设置legend(设置位置)
    # 位置在左上角
    plt.legend(loc='upper left')
    # 添加网格
    plt.grid(color="k", linestyle=":")
    plt.show()
def main():
    op_main()
def extract_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('07-03') and 'lens_pos=' in line:
            parts = line.split(' ')
            lens_pos = None
            pd = None

            for part in parts:
                if 'lens_pos=' in part:
                    lens_pos = int(part.split('=')[1])
                elif 'defocus(um)=' in part:
                    pd = float(part.split('=')[1].strip(','))

            if lens_pos is not None and pd is not None:
                data[lens_pos] = pd

    # 获取最下面的defocus值
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    result = {k: v for k, v in sorted_data}

    return result

if __name__ =="__main__":
    main()
