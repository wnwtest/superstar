# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:18:14 2020

@author: tony
"""

import  os
import time
 

 
text = os.popen("adb root")
time.sleep(1)
print (text.read())

text = os.popen("adb remount")
time.sleep(1)
print (text.read())

flies = os.listdir(".");
for ff in flies:
    if (ff.endswith('.so')):
        print ("adb push " + ff +" /system/vendor/lib/")
        text = os.popen("adb push " + ff +" /system/vendor/lib/")
        time.sleep(1)
        print (text.read())

text = os.popen("adb reboot")
time.sleep(1)
print (text.read())