import subprocess
import time

print("------start------")

count = 100

def check_boot():
    while True:
        result = subprocess.run(['adb', 'logcat', '-d'], stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore')
        if "Finished processing BOOT_COMPLETED for u0" in result:
            print("Device finished booting")
            break
        else:
            print("Waiting for device to finish booting...")
            time.sleep(3)

def check_scan_result():
    while True:
        result = subprocess.run(['adb', 'logcat', '-d'], stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore')
        if "getresult =" in result:
            print("scanner ok")
            break
        else:
            print("Waiting for scanner result")
            time.sleep(3)

for i in range(1, count+1):
    print(f"第{i}次")
    subprocess.run(['adb', 'reboot'])
    time.sleep(20)
    check_boot()
    subprocess.run(['adb', 'shell', 'input', 'swipe', '640', '700', '640', '20'])
    time.sleep(1)
    subprocess.run(['adb', 'shell', 'am', 'start', '-n', 'com.ubx.scandemo/.ScanDemoActivity'])
    time.sleep(2)
    subprocess.run(['adb', 'shell', 'input', 'tap', '539', '1182'])
    time.sleep(2)
    check_scan_result()

print("------end------")