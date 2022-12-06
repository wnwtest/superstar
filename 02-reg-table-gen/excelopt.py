#-*- coding=utf-8 -*-
import xlrd
excel_path = "F:\\2020\\SQ53_model\\data.xlsx"
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_byname(by_name=u'Sheet1'):#修改自己路径
     file = u'F:\\2020\\SQ53_model\\data.xlsx'
     data = open_excel(file)
     table = data.sheet_by_name(by_name) #获得表格
     nrows = table.nrows  # 拿到总共行数
     print(nrows)
     colnames = table.row_values(2)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
     for i in range(len(colnames)):
         print (colnames[i])

     list = []
     for rownum in range(3, nrows): #也就是从Excel第二行开始，第一行表头不算
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                 app[colnames[i]] = row[i] #表头与数据对应
             list.append(app)
     op_write_arrage2file(list,by_name)
     return list
def op_write_arrage2file(list, name) :
    key1 = 'register'
    key2 = 'value'
    for row in list:
        print(row[key1])
        print(row[key2])
        print("    {0x"+row[key1]+",  "+"0x"+row[key2]+",  "+"0x00}, "+"\\")
    file = "data_arrange"+name+".txt"
    with open(file,"w") as f:
        for row in list:
            f.write("    {0x" + row[key1] + ",  " + "0x" + row[key2] + ",  " + "0x00}, " + "\\\n")

def main():
    excel_table_byname()
    excel_table_byname(u'Sheet2')
    excel_table_byname(u'Sheet3')
    excel_table_byname(u'Sheet4')
    excel_table_byname(u'Sheet5')
    excel_table_byname(u'Sheet6')
    #op_write_arrage2file(tables)


if __name__ =="__main__":
    main()

