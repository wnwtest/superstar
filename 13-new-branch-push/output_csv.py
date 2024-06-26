# -*- coding: utf-8 -*-
import csv
import os

# 你的数组
list_of_paths = [
                os.path.abspath("external/chromium-webview"),
                os.path.abspath("external/curl"),
                os.path.abspath("external/linux-kselftest"),
                os.path.abspath("external/subsampling-scale-image-view"),
                os.path.abspath("external/timezone-boundary-builder"),
                os.path.abspath("kernel/prebuilts/5.10/arm64"),
                os.path.abspath("kernel/prebuilts/common-modules/virtual-device/5.10/arm64"),
                os.path.abspath("packages/modules/ArtPrebuilt"),
                os.path.abspath("prebuilts/abi-dumps/ndk"),
                os.path.abspath("prebuilts/abi-dumps/platform"),
                os.path.abspath("prebuilts/abi-dumps/vndk"),
                os.path.abspath("prebuilts/android-emulator"),
                os.path.abspath("prebuilts/asuite"),
                os.path.abspath("prebuilts/bazel/common"),
                os.path.abspath("prebuilts/bazel/darwin-x86_64"),               
                os.path.abspath("prebuilts/bazel/linux-x86_64"),
                os.path.abspath("prebuilts/build-tools"),
                os.path.abspath("prebuilts/bundletool"),
                os.path.abspath("prebuilts/checkcolor"),
                os.path.abspath("prebuilts/checkstyle"),
                os.path.abspath("prebuilts/cmdline-tools"),
                os.path.abspath("prebuilts/devtools"),
                os.path.abspath("prebuilts/gcc/linux-x86/host/x86_64-linux-glibc2.17-4.8"),
                os.path.abspath("prebuilts/gcc/linux-x86/host/x86_64-w64-mingw32-4.8"),
                os.path.abspath("prebuilts/go/darwin-x86"),
                os.path.abspath("prebuilts/go/linux-x86"),
                os.path.abspath("prebuilts/gradle-plugin"),
                os.path.abspath("prebuilts/jdk/jdk11"),
                os.path.abspath("prebuilts/jdk/jdk17"),
                os.path.abspath("prebuilts/jdk/jdk8"),
                os.path.abspath("prebuilts/jdk/jdk9"),
                os.path.abspath("prebuilts/ktlint"),
                os.path.abspath("prebuilts/manifest-merger"),
                os.path.abspath("prebuilts/maven_repo/bumptech"),
                os.path.abspath("prebuilts/misc"),
                os.path.abspath("prebuilts/module_sdk/AdServices"),
                os.path.abspath("prebuilts/module_sdk/AppSearch"),
                os.path.abspath("prebuilts/module_sdk/Bluetooth"),
                os.path.abspath("prebuilts/module_sdk/ConfigInfrastructure"),
                os.path.abspath("prebuilts/module_sdk/Connectivity"),
                os.path.abspath("prebuilts/module_sdk/HealthFitness"),
                os.path.abspath("prebuilts/module_sdk/IPsec"),
                os.path.abspath("prebuilts/module_sdk/Media"),
                os.path.abspath("prebuilts/module_sdk/MediaProvider"),
                os.path.abspath("prebuilts/module_sdk/OnDevicePersonalization"),
                os.path.abspath("prebuilts/module_sdk/Permission"),
                os.path.abspath("prebuilts/module_sdk/RemoteKeyProvisioning"),
                os.path.abspath("prebuilts/module_sdk/Scheduling"),
                os.path.abspath("prebuilts/module_sdk/SdkExtensions"),
                os.path.abspath("prebuilts/module_sdk/StatsD"),
                os.path.abspath("prebuilts/module_sdk/Uwb"),  
                os.path.abspath("prebuilts/module_sdk/Wifi"),
                os.path.abspath("prebuilts/module_sdk/art"),
                os.path.abspath("prebuilts/module_sdk/conscrypt"),
                os.path.abspath("prebuilts/ndk"),
                os.path.abspath("prebuilts/qemu-kernel"),
                os.path.abspath("prebuilts/r8"),
                os.path.abspath("prebuilts/remoteexecution-client"),
                os.path.abspath("prebuilts/runtime"),
                os.path.abspath("prebuilts/tools"),
                os.path.abspath("prebuilts/vndk/v29"), 
                os.path.abspath("prebuilts/vndk/v30"),
                os.path.abspath("prebuilts/vndk/v31"),
                os.path.abspath("prebuilts/vndk/v32"),
                os.path.abspath("prebuilts/vndk/v33"),
                os.path.abspath("tools/tradefederation/prebuilts"),
                os.path.abspath("vendor/rockchip/hardware/interfaces/tv"),                                    
]

# 将数组转换为CSV格式
with open('paths.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Absolute Path'])  # 写入标题
    for path in list_of_paths:
        writer.writerow([os.path.abspath(path)])  # 写入每个路径的绝对路径