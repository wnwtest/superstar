#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import shutil
import zipfile
import re

try:
    input = raw_input  # Python 2
except NameError:
    pass  # Python 3

def safe_makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\.]', '_', filename)

def generate_android_mk(app_name, lib_files):
    config = """LOCAL_PATH := $(my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := {0}
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := {0}.apk
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_MODULE_PATH := $(TARGET_OUT_PRODUCT)/third-app
LOCAL_REPLACE_PREBUILT_APK_INSTALLED := $(LOCAL_PATH)/$(LOCAL_MODULE).apk
LOCAL_DEX_PREOPT := false
""".format(app_name)

    if lib_files:
        config += "LOCAL_MULTILIB := both\n"
        config += "LOCAL_PREBUILT_JNI_LIBS := \\\n"
        for arch, libs in lib_files.items():
            for lib in libs:
                config += "\tlib/{}/{} \\\n".format(arch, lib)
    else:
        config += "LOCAL_MULTILIB := 64\n"
        config += "LOCAL_MODULE_TARGET_ARCH := arm64\n"

    config += "\ninclude $(BUILD_PREBUILT)"
    return config

def process_apk(apk_path, output_dir):
    app_name = os.path.splitext(os.path.basename(apk_path))[0]
    safe_app_name = sanitize_filename(app_name)
    app_dir = os.path.join(output_dir, safe_app_name)
    safe_makedirs(app_dir)

    # Copy APK file
    shutil.copy2(apk_path, os.path.join(app_dir, safe_app_name + '.apk'))

    # Extract lib files if exist
    lib_files = {}
    #architectures = ['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64']
    architectures = ['arm64-v8a', 'armeabi-v7a']
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            for arch in architectures:
                if file.startswith('lib/{}/'.format(arch)):
                    if arch not in lib_files:
                        lib_files[arch] = []
                    lib_files[arch].append(os.path.basename(file))
                    zip_ref.extract(file, app_dir)

    # Generate Android.mk
    android_mk = generate_android_mk(safe_app_name, lib_files)
    with open(os.path.join(app_dir, 'Android.mk'), 'w') as f:
        f.write(android_mk)

    return safe_app_name

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <apk_directory>")
        sys.exit(1)

    apk_dir = sys.argv[1]
    output_dir = 'output'
    safe_makedirs(output_dir)

    preload_modules = []

    for filename in os.listdir(apk_dir):
        if filename.endswith('.apk'):
            apk_path = os.path.join(apk_dir, filename)
            app_name = process_apk(apk_path, output_dir)
            preload_modules.append(app_name)

    # Generate preload.mk
    with open(os.path.join(output_dir, 'preload.mk'), 'w') as f:
        f.write("PRODUCT_PACKAGES += \\\n")
        for module in preload_modules:
            f.write("\t{} \\\n".format(module))

    print("Processing completed. Output directory: {}".format(output_dir))

if __name__ == "__main__":
    main()