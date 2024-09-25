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

def sanitize_filename(filename):
    # Remove any character that isn't a letter, number, underscore, or hyphen
    return re.sub(r'[^\w\-_\.]', '_', filename)

def generate_android_mk(app_name, lib_files):
    config = """LOCAL_PATH := $(my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := {0}
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := {1}.apk
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_MODULE_PATH := $(TARGET_OUT_PRODUCT)/third-app
LOCAL_REPLACE_PREBUILT_APK_INSTALLED := $(LOCAL_PATH)/$(LOCAL_MODULE).apk
LOCAL_DEX_PREOPT := false
LOCAL_MODULE_TARGET_ARCH := arm64
LOCAL_MULTILIB := 64
""".format(app_name, os.path.splitext(os.path.basename(app_name))[0])

    if lib_files:
        config += "LOCAL_PREBUILT_JNI_LIBS := \\\n"
        for lib_file in lib_files:
            config += "\tlib/arm64-v8a/{} \\\n".format(lib_file)

    config += "\ninclude $(BUILD_PREBUILT)"
    return config

def process_apk(apk_path, output_dir):
    app_name = os.path.splitext(os.path.basename(apk_path))[0]
    safe_app_name = sanitize_filename(app_name)
    app_dir = os.path.join(output_dir, safe_app_name)
    os.makedirs(app_dir, exist_ok=True)

    # Copy APK file
    shutil.copy2(apk_path, os.path.join(app_dir, safe_app_name + '.apk'))

    # Extract lib files if exist
    lib_files = []
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith('lib/arm64-v8a/'):
                lib_files.append(os.path.basename(file))
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
    os.makedirs(output_dir, exist_ok=True)

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