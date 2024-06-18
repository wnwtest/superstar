# -*- coding: utf-8 -*-
import os
import sys
import subprocess

# 请在此列表中添加需要忽略的项目路径
ignore_list = [ os.path.abspath("external/chromium-webview"),
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

def get_remote_name(repo_path):
    output = subprocess.check_output(['git', '-C', repo_path, 'remote', '-v'])
    lines = output.split('\n')
    remote_name = lines[0].split('\t')[0]
    return remote_name

def push_with_retry(repo_path, branch_name):
    success = False
    while not success:
        try:
            remote_name = get_remote_name(repo_path)
            output = subprocess.check_output(['git', '-C', repo_path, 'push', remote_name, 'HEAD:{}'.format(branch_name)], stderr=subprocess.STDOUT)
            success = True
            print('Successfully pushed {} to {} in {}'.format(branch_name, remote_name, repo_path))
        except subprocess.CalledProcessError as e:
            error_message = e.output
            print('Push to {} in {} failed with error: {}'.format(remote_name, repo_path, error_message))
            if 'Could not read from remote repository' in error_message or 'incorrect signature' in error_message:
                print('Retry pushing due to error: {}'.format(error_message))
                success = False
            else:
                raise e
    return success

def main():
    if len(sys.argv) < 2:
        print('Please provide the new branch name as a command line argument.')
        sys.exit(1)

    new_branch = sys.argv[1]

    output = subprocess.check_output(['./repo/repo', 'forall', '-c', 'pwd'])
    repo_paths = output.split('\n')[:-1]  # Remove the last empty string

    failed_repos = []
    for repo_path in repo_paths:
        if repo_path in ignore_list:  # 忽略列表中的仓库
            print('Skipping push for {}'.format(repo_path))
            continue
        success = push_with_retry(repo_path, new_branch)
        if not success:
            failed_repos.append(repo_path)

    while failed_repos:
        for repo_path in failed_repos[:]:
            print('Retrying push for {}'.format(repo_path))
            if repo_path in ignore_list:  # 忽略列表中的仓库
                print('Skipping retry push for {}'.format(repo_path))
                failed_repos.remove(repo_path)
                continue
            #print('Retrying push for {}'.format(repo_path))
            success = push_with_retry(repo_path, new_branch)
            if success:
                failed_repos.remove(repo_path)

    print('Push completed. {} repositories failed to push.'.format(len(failed_repos)))

if __name__ == '__main__':
    main()