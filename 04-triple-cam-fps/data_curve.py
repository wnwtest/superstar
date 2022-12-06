#-*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
import re

plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False # 用来正常显示负号

def op_main(by_name=u'Sheet1'):
    file0 = "data_cam0.txt"
    file1 = "data_cam1.txt"
    file2 = "data_cam2.txt"
    y0_data = []
    y1_data = []
    y2_data = []
    with open(file0, "r") as f:
        for row in f.readlines():
            #print(row)
            get_value_of_fps(row,y0_data)
    with open(file1, "r") as f:
        for row in f.readlines():
            #print(row)
            get_value_of_fps(row,y1_data)
    with open(file2, "r") as f:
        for row in f.readlines():
            #print(row)
            get_value_of_fps(row,y2_data)
    #print("y:", y0_data)
    calc_real_time_y(y0_data)
    #print("y:", y0_data)
    calc_real_time_y(y1_data)
    calc_real_time_y(y2_data)
    x0=range( len(y0_data) )
    x1 = range(len(y1_data))
    x2 = range(len(y2_data))
    y0 = y0_data
    y1 = y1_data
    y2 = y2_data
    '''
    坐标范围
    总结一下，下面形式的函数可以控制图像的绘图范围：
    plt.axis([x_min, x_max, y_min, y_max])
    如果只是单独想要控制x轴或者y轴的取值，则可以用plt.xlim(x_min, x_max)和plt.ylim(y_min, y_max)，用法与plt.axis()类似。
    '''
    y0_min =900
    y0_max=1200
    plt.ylim(y0_min, y0_max)
    '''
    坐标标题
    plt.xlabel()和plt.xlabel()用来实现对x轴和y轴添加标题
    '''
    plt.xlabel("帧数")
    plt.ylabel("每25帧所花费时间（ms）")
    '''
    坐标间隔设定
    函数plt.xticks()和plt.xticks()用来实现对x轴和y轴坐标间隔（也就是轴记号）的设定。用法上，函数的输入是两个列表，第一个表示取值，第二个表示标记。当然如果你的标记就是取值本身，则第二个列表可以忽略
    '''
    #plt.yticks([i for i in range(y_min,y_max)])

    plt.title("fps 分布图")
    # plot函数作图
    #plt.plot(x0,y0 , color="r", linestyle="--", marker="*", linewidth=1.0)
    #plt.plot(x1, y1, color="g", linestyle="--", marker="*", linewidth=1.0)
    #plt.plot(x2, y2, color="b", linestyle="--", marker="*", linewidth=1.0)
    plt.plot( y0, color="r",label='cam0')
    plt.plot( y1, color="g",label='cam1')
    plt.plot( y2, color="b",label='cam2')
    # 添加文字
    #plt.text(0, 3, "cam0", color="r")
    #plt.text(0, 6, "cam1", color="g")
    #plt.text(0, 9, "cam2", color="b")
    # 简单的设置legend(设置位置)
    # 位置在左上角
    plt.legend(loc='upper left')
    # 添加网格
    plt.grid(color="k", linestyle=":")
    # show函数展示出这个图，如果没有这行代码，则程序完成绘图，但看不到
    plt.show()

def main():
    op_main()
def  get_value_of_fps(line,y):
    #line = "Cats are smarter than dogs";
    value =int(line.strip()[-13:])
    #print("searchObj",value)
    y.append(value)



def calc_real_time_y(data):

    for index in range( len(data) ):
        if( index > 0 ) :
            temp=data[index-1]
            data[index-1]=data[index]-data[index-1]
    data[len(data)-1] -= temp

if __name__ =="__main__":
    main()
