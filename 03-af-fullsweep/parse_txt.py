#-*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
#支持中文显示
plt.rcParams["font.sans-serif"]=["SimHei"]


def str2float(s):
    return reduce(lambda x,y:x+int2dec(y),map(str2int,s.split('.')))
def char2num(s):
    return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
def str2int(s):
    return reduce(lambda x,y:x*10+y,map(char2num,s))
def intLen(i):
    return len('%d'%i)
def int2dec(i):
    return i/(10**intLen(i))

def op_main(by_name=u'Sheet1'):
    file = "af_fullsweep_10cm.log"
    x_data = []
    y_data = []
    tmp = []
    with open(file, "r") as f:
        for row in f.readlines():
            #print(row.split( ','))
            for key in row.split( ','):
                #print(key)
                parse_output(key,x_data,y_data)
    x = np.array(x_data)
    for i in range (len(y_data)):
        #print(y_data[i])
        tmp.append( str2float(y_data[i]))

    y = np.array(y_data)
    #my_y_ticks = np.arange(8600, 8800, 10)
    #plt.plot(x, tmp)
    plt.bar(x, tmp)  
    #plt.yticks(my_y_ticks)
    plt.title("马达 扫描FV分布图")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.show()
def main():
    op_main()
def  parse_output(target,x,y):
    key1 = "Index "
    key2 = "H1 "
    key3 = "H1_norm "
    key4 = "V "
    key5 = "V_norm "
    key6 = "HV "
    key7 = "HV_norm "
    key8 = "LensPosition "
    get_x_index(target, key1,x)
    get_y_index(target,key2,y)

def get_x_index (target,key1,x) :

    if ( target.find(key1) != -1) :
        x.append(target[target.find(key1) + len(key1):])
        #print (target[target.find(key1) + len(key1):])
def get_y_index (target,key1,y) :

    if ( target.find(key1) != -1) :
        y.append(target[target.find(key1) + len(key1):])
        #print (target[target.find(key1) + len(key1):])

if __name__ =="__main__":
    main()
