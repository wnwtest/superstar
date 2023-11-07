ifeq ($(CAMX_CHICDK_PATH),)
LOCAL_PATH := $(abspath $(call my-dir)/../..)
CAMX_CHICDK_PATH := $(abspath $(LOCAL_PATH)/../..)
else
LOCAL_PATH := $(CAMX_CHICDK_PATH)/test/uart-loopback-test
endif

include $(CLEAR_VARS)

# Module supports function call tracing via ENABLE_FUNCTION_CALL_TRACE
# Required before including common.mk
SUPPORT_FUNCTION_CALL_TRACE := 1

# Get definitions common to the CAMX project here
include $(CAMX_CHICDK_PATH)/core/build/android/common.mk

LOCAL_SRC_FILES :=                          \
    uart-loopback.c                    
LOCAL_INC_FILES :=                          \

# Put here any libraries that should be linked by CAMX projects
LOCAL_C_LIBS := $(CAMX_C_LIBS)



# Compiler flags
LOCAL_CFLAGS := $(CAMX_CFLAGS)
LOCAL_CFLAGS += -fno-exceptions         \
                -g                      \
                -Wno-unused-variable

LOCAL_CFLAGS += -DFEATURE_XMLLIB

LOCAL_CPPFLAGS := $(CAMX_CPPFLAGS)

# Defining targets
ifeq ($(TARGET_BOARD_PLATFORM), lahaina)
    LOCAL_CFLAGS += -DTARGET_LAHAINA
endif

ifeq ($(TARGET_BOARD_PLATFORM), kona)
    LOCAL_CFLAGS += -DTARGET_KONA
endif

# Defining Android platform
ifeq ($(ANDROID_FLAVOR), $(ANDROID_FLAVOR_Q))
    LOCAL_CFLAGS += -DPLATFORM_VERSION_Q
endif

ifeq ($(ANDROID_FLAVOR), $(ANDROID_FLAVOR_R))
    LOCAL_CFLAGS += -DPLATFORM_VERSION_R
endif

# Libraries to statically link
LOCAL_STATIC_LIBRARIES :=


LOCAL_SHARED_LIBRARIES := \
        libc \
        libcutils \
        libutils


LOCAL_LDLIBS :=                 \
    -llog                       \
    -lz                         \
    -ldl

LOCAL_LDFLAGS :=

# Binary name
LOCAL_MODULE := uart-loopback-test

# Deployment path under bin
LOCAL_MODULE_RELATIVE_PATH := ../bin
LOCAL_PROPRIETARY_MODULE := true
include $(BUILD_EXECUTABLE)
