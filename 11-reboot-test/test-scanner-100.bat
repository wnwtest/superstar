@echo off

echo ------start------

set count=100

for /l %%i in (1,1,%count%) do (

	echo µÚ%%i%´Î
    adb reboot
    ping -n 20 127.0.0.1>nul
    call :checkBoot
    adb shell input swipe 640 700 640 20
    ping -n 1 127.0.0.1>nul
    adb shell am start -n com.ubx.scandemo/.ScanDemoActivity
    ping -n 2 127.0.0.1>nul
    adb shell input tap 539 1182
    ping -n 2 127.0.0.1>nul
    call :checkScanResult
)

echo ------end------
pause
exit /b

:checkBoot
    :loop
        adb logcat -d | findstr /C:"Finished processing BOOT_COMPLETED for u0"
        if errorlevel 1 (
            echo Waiting for device to finish booting...
            timeout /t 3
            goto loop
        ) else (
            echo Device finished booting            
        )
    exit /b

:checkScanResult
    :loop2
        adb logcat -d | findstr /C:"getresult ="
        if errorlevel 1 (
            echo Waiting for scanner result
            timeout /t 3
            goto loop2
        ) else (
            echo scanner ok  
        )
    exit /b