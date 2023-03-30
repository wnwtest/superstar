#coding=utf-8
import  xml.dom.minidom

def  driver_initsettings_check( ) :
    # 打开xml文档
    dom = xml.dom.minidom.parse('hi1336_sensor.xml')
    # 得到文档元素对象
    rootNote = dom.documentElement
    print("rootNote", rootNote.nodeName)
    resolutionInfo = rootNote.getElementsByTagName('initSettings')
    value1 = resolutionInfo[0]
    print("sub node 1", value1.nodeName)
    initSetting = value1.getElementsByTagName('initSetting')
    res_resSettings_value = initSetting[0];
    #print("res 0", res0_resSettings_value.nodeName)

    res_regSetting = res_resSettings_value.getElementsByTagName('regSetting')
    #print("res 0 res size", len(res0_regSetting))
    reg_size = len(res_regSetting)
    print("init reg size", reg_size )
    for i in range(reg_size):
        res_resSetting_value = res_regSetting[i];
        #print("res 0", res0_resSetting_value.nodeName)
        #print("dump reg info")
        #print("reg 0 ", res0_resSetting_value.nodeValue)
        registerAddr = res_resSetting_value.getElementsByTagName('registerAddr')
        addr = registerAddr[0]
        #print("addr ", addr.firstChild.data)
        registerData = res_resSetting_value.getElementsByTagName('registerData')
        data = registerData[0]
        #print("data", data.firstChild.data)
        print("addr:",addr.firstChild.data," data:",data.firstChild.data)



def  driver_resolution_check( res_value) :
    # 打开xml文档
    dom = xml.dom.minidom.parse('hi1336_sensor.xml')
    # 得到文档元素对象
    rootNote = dom.documentElement
    print("rootNote", rootNote.nodeName)
    resolutionInfo = rootNote.getElementsByTagName('resolutionInfo')
    value1 = resolutionInfo[0]
    print("sub node 1", value1.nodeName)
    resolutionData = value1.getElementsByTagName('resolutionData')
    # Res0 4160x3120
    res = resolutionData[res_value]
    #print( "res length",len(resolutionData))
    print("res",res_value ,res.nodeName)
    res_resSettings = res.getElementsByTagName('resSettings')
    res_resSettings_value = res_resSettings[0];
    #print("res 0", res0_resSettings_value.nodeName)

    res_regSetting = res_resSettings_value.getElementsByTagName('regSetting')
    #print("res 0 res size", len(res0_regSetting))
    reg_size = len(res_regSetting)
    print("res", res_value, " reg size", reg_size )

    for i in range(reg_size):
        res_resSetting_value = res_regSetting[i];
        #print("res 0", res0_resSetting_value.nodeName)
        #print("dump reg info")
        #print("reg 0 ", res0_resSetting_value.nodeValue)
        registerAddr = res_resSetting_value.getElementsByTagName('registerAddr')
        addr = registerAddr[0]
        #print("addr ", addr.firstChild.data)
        registerData = res_resSetting_value.getElementsByTagName('registerData')
        data = registerData[0]
        #print("data", data.firstChild.data)
        print("addr:",addr.firstChild.data," data:",data.firstChild.data)

def driver_factory_initdata () :
    print ("driver_factory_initdata ")
    file = "init.txt"
    with  open(file,  "r")  as  fileHandler:
        # Read next line
        line  =  fileHandler.readline()
        # check line is not empty
        while  line:
             #print(line.strip())
             data = line.strip()
             addr1 = data[1:7]
             data1 = data[8:15]
             print("addr:",addr1," data:",data1)

             line  =  fileHandler.readline()

def driver_factory_data (res_value) :
    print ("driver_factory_data ")
    file = "res"+str(res_value)+".txt"
    with  open(file,  "r")  as  fileHandler:
        # Read next line
        line  =  fileHandler.readline()
        # check line is not empty
        while  line:
             #print(line.strip())
             data = line.strip()
             addr1 = data[1:7]
             data1 = data[8:15]
             print("addr:",addr1," data:",data1)

             line  =  fileHandler.readline()
def  main():
    index = 4
    driver_resolution_check(index)
    driver_factory_data(index)
    #driver_initsettings_check()
    #driver_factory_initdata()

if __name__ == "__main__":
    main()