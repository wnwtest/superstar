ifneq (,$(filter arm aarch64 arm64, $(TARGET_ARCH)))

LOCAL_PATH := $(CAMX_CHICDK_PATH)/test/msm_uart_test

include $(CLEAR_VARS)
LOCAL_MODULE := msm_uart_test
LOCAL_C_FLAGS := -lpthread
LOCAL_SRC_FILES :=  msm_uart_test.c

LOCAL_SHARED_LIBRARIES := \
        libc \
        libcutils \
        libutils

LOCAL_MODULE_TAGS := optional
# Deployment path under bin
LOCAL_MODULE_RELATIVE_PATH := ../bin
LOCAL_PROPRIETARY_MODULE := true
LOCAL_MODULE_OWNER := qcom
include $(BUILD_EXECUTABLE)



endif
