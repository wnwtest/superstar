# -*- coding: utf-8 -*-
import os
import sys

def generate_config(app_name, lib_folder):
    # 遍历文件夹获取所有库文件
    lib_files = [f for f in os.listdir(lib_folder) if os.path.isfile(os.path.join(lib_folder, f))]

    # 按照给定的格式生成配置
    config = """#generated config
LOCAL_PATH := $(my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := %s
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := %s.apk
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_MODULE_PATH := $(TARGET_OUT_PRODUCT)/third-app
LOCAL_REPLACE_PREBUILT_APK_INSTALLED:=$(LOCAL_PATH)/$(LOCAL_MODULE).apk
LOCAL_DEX_PREOPT := false
LOCAL_MODULE_TARGET_ARCH := arm64
LOCAL_MULTILIB := 64
LOCAL_PREBUILT_JNI_LIBS := \\
""" % (app_name, app_name)

    # 添加所有库文件
    for lib_file in lib_files:
        config += "\tlib/arm64-v8a/%s \\\n" % lib_file

    config += "\ninclude $(BUILD_PREBUILT)"

    # 输出配置到文件
    with open('out.mk', 'w') as f:
        f.write(config)
    print("Makefile has been written to out.mk")
def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_config.py <app_name> <lib_folder>")
        return

    app_name = sys.argv[1]
    lib_folder = sys.argv[2]

    generate_config(app_name, lib_folder)

if __name__ == "__main__":
    main()