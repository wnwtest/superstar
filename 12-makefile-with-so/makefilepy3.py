"""
generate_makefile.py

This script generates an Android makefile for a given APK and its associated shared libraries.

Usage: python generate_makefile.py <apk_name> <so_lib_folder>

License: MIT License

Copyright (c) 2024 <tony wang>

这是一段构建Makefile的Python脚本。脚本的主要功能是根据给定的apk名称（apk_name）和包含.so库的文件夹（so_lib_folder）生成对应的Makefile。
它首先获取文件夹中所有.so文件，然后循环生成每个.so库的配置。然后，生成apk的配置，包括其依赖的.so库。最后，将所有的配置写入一个叫作'out.mk'的文件中。
运行文件的命令应为 python generate_makefile.py <apk_name> <so_lib_folder> 其中，<apk_name> 为你的apk名称，<so_lib_folder>为.so库的文件夹。
文件运行后，会在当前目录生成一个名为 'out.mk' 的Makefile文件

"""

import sys
import os

def generate_makefile(apk_name, so_lib_folder):
    makefile_text = ""
    # List comprehension to gather .so libraries and strip the '.so' extension
    so_libs = [f[:-3] for f in os.listdir(so_lib_folder) if f.endswith('.so')]

    # Generate library configurations
    for lib in so_libs:
        makefile_text += f"""
include $(CLEAR_VARS)
LOCAL_MODULE := {lib}
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := .so
LOCAL_SRC_FILES := lib/arm64-v8a/{lib}.so
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/product/lib64/
include $(BUILD_PREBUILT)
"""

    # Generate apk configuration
    makefile_text += f"""
include $(CLEAR_VARS)
LOCAL_MODULE := {apk_name}
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := {apk_name}.apk
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_MODULE_PATH := $(TARGET_OUT_PRODUCT)/third-app/{apk_name}/
LOCAL_DEX_PREOPT := false
LOCAL_REQUIRED_MODULES := {' '.join(so_libs)}
include $(BUILD_PREBUILT)
"""

    return makefile_text

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python generate_makefile.py <apk_name> <so_lib_folder>")
        return

    # Get apk name and folder of so libraries from command line arguments
    apk_name = sys.argv[1]
    so_lib_folder = sys.argv[2]

    # Generate makefile
    makefile = generate_makefile(apk_name, so_lib_folder)

    # Write makefile to out.mk
    with open('out.mk', 'w') as f:
        f.write(makefile)

    print("Makefile has been written to out.mk")

if __name__ == "__main__":
    main()
