# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import yaml
import argparse
import time
import logging
import traceback

# --- 常量定义 ---
CONFIG_FILE = 'build.yaml'      # u'配置文件名'
GUIDE_FILE = 'repo_guide.txt'   # u'Repo 指南文件名'
DEFAULT_MAX_RETRIES = 3         # u'默认最大重试次数'
DEFAULT_RETRY_DELAY = 5         # u'默认重试间隔（秒）'

# --- 日志配置 ---
# u'移除自定义 Handler，直接配置基础日志记录器'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # u'添加 levelname 以更好地区分信息级别'
    stream=sys.stdout  # u'直接输出到标准输出'
)
logger = logging.getLogger(__name__)
# u'不再需要添加自定义 Handler'

def safe_decode(value):
    # u"""安全解码字节串为 UTF-8 字符串，用于处理 subprocess 输出，兼容 Python 2.7。"""
    if isinstance(value, str): # Python 2的 str 是字节串
        try:
            # u'尝试使用 UTF-8 解码，忽略无法解码的字符'
            return value.decode('utf-8', errors='ignore')
        except Exception as e:
            # u'如果解码失败，记录警告并返回原始字节串'
            logger.warning(u"Failed to decode bytes using UTF-8: {}. Returning original value.".format(e))
            return value
    # u'如果已经是 unicode 或其他类型，直接返回'
    return value

def get_remote_name(repo_path):
    # u"""获取指定 Git 仓库的第一个远程仓库名称（兼容 Python 2.7）。"""
    try:
        # u'执行 git remote -v 命令获取远程仓库信息'
        # u'在 Python 2 中，check_output 返回字节串'
        output_bytes = subprocess.check_output(['git', '-C', repo_path, 'remote', '-v'])
        # u'解码为 Unicode 字符串'
        output = safe_decode(output_bytes)
        lines = output.split('\n')
        if lines and lines[0]:
            # u'通常第一行列出了 origin 或其他远程仓库名和 URL'
            remote_name = lines[0].split('\t')[0]
            return remote_name
        else:
            logger.warning(u"Could not determine remote name for repository: {}".format(repo_path))
            return None # u'无法确定远程名时返回 None'
    except subprocess.CalledProcessError as e:
        error_message = safe_decode(e.output)
        logger.error(u"Error getting remote name for {}: {}".format(repo_path, error_message))
        return None
    except Exception as e:
        logger.error(u"Unexpected error getting remote name for {}: {}".format(repo_path, e))
        return None

# u'重命名函数以更准确反映其功能（推送和删除）'
def manage_remote_branch_with_retry(repo_path, branch_name, delete=False, max_retries=DEFAULT_MAX_RETRIES, retry_delay=DEFAULT_RETRY_DELAY):
    # u"""
    # u'推送或删除远程分支，包含重试逻辑和错误处理。
    # u':param repo_path: 仓库路径
    # u':param branch_name: 分支名称
    # u':param delete: 是否为删除操作 (True 表示删除, False 表示推送)
    # u':param max_retries: 最大重试次数
    # u':param retry_delay: 重试间隔时间（秒）
    # u':return: (success, skip) - (操作是否最终成功, 是否因为分支不存在而被跳过)
    # u"""
    remote_name = get_remote_name(repo_path)
    if not remote_name:
        logger.error(u"Skipping repository {} due to missing remote name.".format(repo_path))
        return False, False # u'无法获取远程名，操作失败'

    action = "delete" if delete else "push"
    action_gerund = "Deleting" if delete else "Pushing" # u'用于日志消息'

    for attempt in range(max_retries + 1):
        try:
            if delete:
                # u'删除操作前先检查远程分支是否存在'
                # u'注意：git ls-remote --exit-code 会在分支不存在时返回非零退出码'
                try:
                    # u'使用 --exit-code 替代检查输出，更健壮'
                    subprocess.check_call(
                        ['git', '-C', repo_path, 'ls-remote', '--exit-code', '--heads', remote_name, branch_name],
                        stderr=subprocess.STDOUT, # u'将 stderr 重定向到 stdout'
                        stdout=subprocess.PIPE # u'隐藏成功的 stdout 输出'
                    )
                    # u'如果上面命令成功（退出码为0），说明分支存在，执行删除'
                    logger.info(u"Attempting to delete branch '{}' from remote '{}' in {}".format(branch_name, remote_name, repo_path))
                    subprocess.check_output(
                        ['git', '-C', repo_path, 'push', remote_name, '--delete', branch_name],
                        stderr=subprocess.STDOUT
                    )
                    logger.info(u"Successfully deleted branch '{}' from remote '{}' in {}".format(branch_name, remote_name, repo_path))

                except subprocess.CalledProcessError as e:
                    # u'如果 ls-remote 返回非零退出码 (通常是 2)，表示远程分支不存在'
                    if e.returncode == 2:
                       logger.info(u"Branch '{}' does not exist on remote '{}' in {}. Skipping delete.".format(branch_name, remote_name, repo_path))
                       return True, True # u'成功（因为目标不存在），标记为跳过'
                    else:
                       # u'ls-remote 因其他原因失败'
                       error_message = safe_decode(e.output)
                       logger.warning(u"Failed to check remote branch existence for '{}' in {}. Error: {}".format(branch_name, repo_path, error_message))
                       # u'继续尝试删除，也许删除命令能处理'
                       logger.info(u"Attempting to delete branch '{}' from remote '{}' in {} despite check failure".format(branch_name, remote_name, repo_path))
                       subprocess.check_output(
                           ['git', '-C', repo_path, 'push', remote_name, '--delete', branch_name],
                           stderr=subprocess.STDOUT
                       )
                       logger.info(u"Successfully deleted branch '{}' from remote '{}' in {}".format(branch_name, remote_name, repo_path))

            else:
                # u'推送操作'
                logger.info(u"Attempting to push branch '{}' to remote '{}' in {}".format(branch_name, remote_name, repo_path))
                # u'使用 HEAD:refs/heads/BRANCH_NAME 强制推送当前 HEAD 到指定远程分支'
                subprocess.check_output(
                    ['git', '-C', repo_path, 'push', remote_name, 'HEAD:refs/heads/%s' % branch_name],
                    stderr=subprocess.STDOUT
                )
                logger.info(u"Successfully pushed to branch '{}' on remote '{}' in {}".format(branch_name, remote_name, repo_path))

            # u'如果执行到这里，表示操作成功'
            return True, False

        except subprocess.CalledProcessError as e:
            # u'Git 命令执行失败'
            error_message = safe_decode(e.output)

            # u'特定错误处理 (删除时)'
            # u'注意: 依赖错误字符串可能比较脆弱，Git 版本更新可能导致消息变化'
            if delete and 'remote ref does not exist' in error_message:
                logger.info(u"Branch '{}' does not exist on remote '{}' in {}. Skipping delete.".format(branch_name, remote_name, repo_path))
                return True, True # u'成功（因为目标不存在），标记为跳过'

            # u'检查是否为已知可重试的网络错误'
            network_errors = [
                'Could not read from remote repository',
                'Connection timed out',
                'Failed to connect',
                'Network is unreachable',
                'fatal: unable to access', # u'常见于 HTTP/HTTPS'
                'Connection refused',
                'ssh_exchange_identification', # u'SSH 连接问题'
                'incorrect signature' # u'有时与网络或代理有关'
            ]
            is_retryable = any(err_keyword in error_message for err_keyword in network_errors)

            if is_retryable and attempt < max_retries:
                logger.warning(u"Attempt {}/{} failed for {} branch '{}' in {}. Error: {}. Retrying in {} seconds...".format(
                    attempt + 1, max_retries + 1, action, branch_name, repo_path, error_message.strip(), retry_delay))
                time.sleep(retry_delay)
                continue # u'继续下一次重试'
            else:
                # u'达到最大重试次数或错误不可重试'
                logger.error(u"Failed to {} branch '{}' in {} after {} attempts. Final error: {}".format(
                    action, branch_name, repo_path, attempt + 1, error_message.strip()))
                return False, False # u'操作失败'

        except Exception as e:
            # u'捕获其他意外错误'
            logger.error(u"An unexpected error occurred during {} for branch '{}' in {}: {}".format(
                action, branch_name, repo_path, traceback.format_exc()))
            return False, False # u'操作失败'

    # u'如果循环结束仍未成功（理论上不应到这里，除非 max_retries < 0）'
    return False, False

def validate_build_yaml(yaml_path=CONFIG_FILE):
    # u"""验证 build.yaml 文件的结构和必需字段是否存在。"""
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            logger.error(u"Invalid format: {} should contain a dictionary.".format(yaml_path))
            return False

        # u'定义必须存在的嵌套键路径'
        required_key_paths = [
            ('project', 'model', 'internal'),
            ('project', 'model', 'external'),
            ('project', 'chip', 'platform'),
            ('project', 'version', 'android'),
            ('project', 'date'),
            ('project', 'baseline'),
            # u'虽然 repo_root_path 是可选的，但如果提供了，project 键必须存在'
            # u'如果它不存在，我们在 get_repo_root_path_from_yaml 中有后备逻辑'
            ('project',)
        ]

        # u'检查每个必需的路径'
        for key_path in required_key_paths:
            current_level = config
            valid_path = True
            for i, key in enumerate(key_path):
                if isinstance(current_level, dict) and key in current_level:
                    current_level = current_level[key]
                else:
                    logger.error(u"Missing required configuration key path in {}: '{}'".format(
                        yaml_path, ' -> '.join(key_path[:i+1])))
                    valid_path = False
                    break # u'此路径无效，检查下一个'
            if not valid_path:
                return False # u'有一个必需路径缺失，验证失败'

        logger.info(u"{} validation successful.".format(yaml_path))
        return True

    except yaml.YAMLError as e:
        logger.error(u"Error parsing {}: {}".format(yaml_path, e))
        return False
    except IOError as e:
        logger.error(u"Error reading {}: {}".format(yaml_path, e))
        return False
    except Exception as e:
        # u'捕获其他潜在错误，例如文件权限问题等'
        logger.error(u"An unexpected error occurred during validation of {}: {}".format(yaml_path, e))
        return False

def get_repo_root_path_from_yaml(yaml_path=CONFIG_FILE):
    # u"""
    # u'从 YAML 文件中获取 repo 根目录路径。
    # u'如果 YAML 中未指定，则使用当前脚本所在目录的父目录作为备选。
    # u'Args:
    # u'    yaml_path (str): YAML 文件路径
    # u'Returns:
    # u'    str: repo 根目录的绝对路径，如果无法确定或无效则返回 None
    # u"""
    repo_root_path = None
    try:
        # u'尝试从 YAML 读取路径'
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            if isinstance(config, dict):
                # u'安全地获取嵌套键的值'
                repo_root_path = config.get('project', {}).get('repo_root_path')

        # u'如果 YAML 中未指定路径或文件不存在，则使用脚本位置推断'
        if not repo_root_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # u'假设脚本位于 repo 根目录下的某个子目录（例如 build/tools）'
            # u'取脚本目录的父目录作为可能的 repo 根目录'
            inferred_path = os.path.dirname(script_dir)
            logger.info(u"Repo root path not found in {}, inferring from script location: {}".format(yaml_path, inferred_path))
            repo_root_path = inferred_path
        else:
             logger.info(u"Repo root path found in {}: {}".format(yaml_path, repo_root_path))

        # u'转换为绝对路径'
        repo_root_path = os.path.abspath(repo_root_path)

        # u'验证推断出的路径是否是一个有效的 repo 工作区（包含 .repo 目录）'
        if os.path.isdir(repo_root_path) and os.path.exists(os.path.join(repo_root_path, '.repo')):
            logger.info(u"Confirmed repo root at: {}".format(repo_root_path))
            return repo_root_path
        else:
            logger.error(u"Validation failed: '{}' is not a valid repo root directory (missing .repo).".format(repo_root_path))
            return None

    except yaml.YAMLError as e:
        logger.error(u"Error parsing {} while getting repo root path: {}".format(yaml_path, e))
        return None
    except IOError as e:
        # u'如果 YAML 文件存在但无法读取，记录错误但继续尝试基于脚本位置推断'
        logger.warning(u"Could not read {}: {}. Will attempt to infer path from script location.".format(yaml_path, e))
        # u'确保 repo_root_path 在这里是 None 或之前的推断值'
        if not repo_root_path: # u'如果之前没有从文件读取成功且没有推断过'
             script_dir = os.path.dirname(os.path.abspath(__file__))
             inferred_path = os.path.dirname(script_dir)
             logger.info(u"Inferring repo root path from script location: {}".format(inferred_path))
             repo_root_path = inferred_path
             # u'再次验证推断的路径'
             repo_root_path = os.path.abspath(repo_root_path)
             if os.path.isdir(repo_root_path) and os.path.exists(os.path.join(repo_root_path, '.repo')):
                 logger.info(u"Confirmed repo root at: {}".format(repo_root_path))
                 return repo_root_path
             else:
                 logger.error(u"Validation failed: '{}' (inferred) is not a valid repo root directory.".format(repo_root_path))
                 return None
        # u'如果之前有值（例如从文件读取成功，但后来发生IOError? 不太可能，但为了安全）'
        # u'只需返回已有的 repo_root_path （或 None）'
        return repo_root_path # 或者 return None 如果路径无效

    except Exception as e:
        logger.error(u"An unexpected error occurred retrieving the repo root path: {}".format(e))
        return None


def safe_str(value):
    # u"""确保值被安全地转换为字符串，处理 None 和可能的集合类型。"""
    if value is None:
        return ''
    # u'假设集合类型（如 set）在 YAML 中用于单一值时，取其第一个元素'
    # u'这通常是为了处理 YAML 中可能出现的 `!!set {value: null}` 格式'
    if isinstance(value, set):
        try:
            # u'尝试获取集合的第一个元素'
            first_element = next(iter(value))
            return safe_str(first_element) # u'递归调用以处理嵌套或去除引号'
        except StopIteration:
             # u'集合为空'
             return ''
    # u'处理 Python 2 的字节串和 Unicode 字符串'
    if isinstance(value, basestring):
        # u'移除可能由 YAML 解析或用户输入引入的多余引号'
        return value.strip('"\'')
    # u'对于其他类型（如数字、布尔值），直接转换为字符串'
    return str(value)


def parse_build_yaml(yaml_path=CONFIG_FILE):
    # u"""解析 build.yaml 文件以生成分支名、基线和外部模型名。"""
    if not os.path.exists(yaml_path):
        logger.error(u"Configuration file '{}' not found.".format(yaml_path))
        return None, None, None
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict) or 'project' not in config:
             logger.error(u"Invalid configuration format in {}. Missing 'project' key.".format(yaml_path))
             return None, None, None

        # u'获取配置值，使用 .get() 提供默认值以避免 KeyError'
        project_config = config.get('project', {})
        model_config = project_config.get('model', {})
        chip_config = project_config.get('chip', {})
        version_config = project_config.get('version', {})

        # u'使用 safe_str 处理每个组件，确保它们是干净的字符串'
        model_internal = safe_str(model_config.get('internal'))
        model_ext = safe_str(model_config.get('external')) # u'外部模型名也用于 manifest 文件名'
        platform = safe_str(chip_config.get('platform'))
        android_version = safe_str(version_config.get('android'))
        date_str = safe_str(project_config.get('date')) # u'假设日期是字符串'
        baseline = safe_str(project_config.get('baseline'))

        # u'构建分支名组件列表'
        branch_components = [
            model_internal,
            model_ext,
            platform,
            android_version,
            date_str
        ]

        # u'过滤掉空字符串组件'
        branch_components_filtered = [comp for comp in branch_components if comp]

        if not branch_components_filtered:
            logger.error(u"No valid components found in {} to generate branch name.".format(yaml_path))
            return None, None, None

        # u'使用下划线连接非空组件生成分支名'
        branch_name = "_".join(branch_components_filtered)

        # u'如果基线为空，提供一个默认值或记录错误？当前策略是允许空基线传出'
        if not baseline:
             logger.warning(u"Baseline is not defined in {}. Repo guide generation might be incomplete.".format(yaml_path))
             # baseline = "default_baseline" # u'或者设置一个默认值'

        logger.info(u"Parsed branch name components: {}".format(branch_components_filtered))
        logger.info(u"Generated branch name: {}".format(branch_name))
        logger.info(u"Baseline: {}".format(baseline or "Not defined"))
        logger.info(u"External model (for manifest): {}".format(model_ext or "Not defined"))

        return branch_name, baseline, model_ext

    except yaml.YAMLError as e:
        logger.error(u"Error parsing {}: {}".format(yaml_path, e))
        return None, None, None
    except IOError as e:
        logger.error(u"Error reading {}: {}".format(yaml_path, e))
        return None, None, None
    except Exception as e:
        logger.error(u"An unexpected error occurred parsing {}: {}".format(yaml_path, traceback.format_exc()))
        return None, None, None


def create_repo_guide(branch_name, baseline, model_ext, output_file=GUIDE_FILE):
    # u"""根据解析出的信息生成 repo 初始化和使用的指导文档。"""
    if not branch_name:
        logger.error(u"Cannot generate repo guide: Branch name is missing.")
        return False
    if not baseline:
        logger.warning(u"Cannot generate repo guide: Baseline is missing. Guide will be incomplete.")
        # u'即使基线缺失，也可能需要生成部分指南，取决于需求'
        # return False  # u'如果基线是绝对必需的，则取消生成'
    if not model_ext:
        logger.warning(u"Cannot generate repo guide: External model name (for manifest) is missing. Guide will be incomplete.")
        # return False # u'如果外部模型名是必需的'

    # u'使用 .format() 进行字符串格式化，兼容 Python 2.7'
    guide_content = u"""Repo Initialization and Sync Guide
===================================

1. Initialize the repository:
   ---------------------------
   repo init -u ssh://your_username@gerrit.example.com:29418/{baseline}/platform/manifest.git \\
   -b {branch_name} -m {model_ext}.xml \\
   --repo-url=ssh://your_username@gerrit.example.com:29418/repo.git \\
   --repo-branch=stable # Or your specific repo tool branch

   * Replace 'your_username' with your Gerrit username.
   * Replace 'gerrit.example.com' with your Gerrit server address.
   * '{baseline}' should be the project baseline (e.g., product_line/project_group). Found: '{baseline_val}'
   * '{branch_name}' is the target branch name. Found: '{branch_name_val}'
   * '{model_ext}.xml' is the manifest file name, derived from the external model name. Found: '{model_ext_val}.xml'

2. Sync the source code:
   ----------------------
   repo sync -j8 # Use '-j' option for parallel download, adjust number as needed

3. Create a development branch (optional but recommended):
   -------------------------------------------------------
   repo start {branch_name}_dev --all # Or choose a more descriptive name

""".format(
        baseline=baseline if baseline else "<BASELINE_MISSING>", # u'在模板中清晰标示缺失值'
        branch_name=branch_name,
        model_ext=model_ext if model_ext else "<MODEL_EXT_MISSING>",
        baseline_val=baseline if baseline else "MISSING",
        branch_name_val=branch_name,
        model_ext_val=model_ext if model_ext else "MISSING"
    )

    try:
        # u'使用 utf-8 编码写入文件，确保兼容性'
        with open(output_file, 'w') as f:
            f.write(guide_content.encode('utf-8')) # 在Python 2中，写入文件通常需要编码
        logger.info(u"Successfully generated repo guide: '{}'".format(output_file))
        return True
    except IOError as e:
        logger.error(u"Failed to write repo guide to '{}': {}".format(output_file, e))
        return False
    except Exception as e:
        logger.error(u"An unexpected error occurred generating repo guide: {}".format(e))
        return False


def get_all_repo_paths(repo_root):
    # u"""在指定的 repo 根目录下，使用 'repo forall -c pwd' 获取所有子仓库的路径。"""
    original_dir = os.getcwd()
    try:
        # u'切换到 repo 根目录以执行 repo 命令'
        os.chdir(repo_root)
        logger.info(u"Running 'repo forall -c pwd' in {}...".format(repo_root))
        # u'执行命令并获取输出（字节串）'
        output_bytes = subprocess.check_output(['repo', 'forall', '-c', 'pwd'])
        # u'解码输出'
        output = safe_decode(output_bytes)
        # u'分割成路径列表，移除可能的空行'
        repo_paths = [path.strip() for path in output.strip().split('\n') if path.strip()]
        logger.info(u"Found {} repositories.".format(len(repo_paths)))
        return repo_paths
    except subprocess.CalledProcessError as e:
        error_message = safe_decode(e.output)
        logger.error(u"Failed to list repositories using 'repo forall'. Error: {}".format(error_message))
        return [] # u'失败时返回空列表'
    except OSError as e:
        # u'例如 repo 命令不存在或切换目录失败'
        logger.error(u"Failed to execute 'repo forall' command. Check if 'repo' is installed and in PATH, and if {} is accessible. Error: {}".format(repo_root, e))
        return []
    except Exception as e:
        logger.error(u"An unexpected error occurred while getting repo paths: {}".format(e))
        return []
    finally:
        # u'确保切回原始目录'
        os.chdir(original_dir)


def main():
    # u'设置参数解析器'
    parser = argparse.ArgumentParser(description='Repository branch management tool (pushes or deletes branch across all repos).')
    # u'可选的位置参数：分支名'
    parser.add_argument('branch', nargs='?', help='(Optional) The name of the branch to push or delete. If omitted, it is derived from build.yaml.')
    # u'互斥的操作选项组'
    group = parser.add_mutually_exclusive_group(required=False) # u'默认操作是从 YAML 推送'
    group.add_argument('--push', action='store_true', help='Explicitly push the branch (default action if branch is from YAML).')
    group.add_argument('--delete', action='store_true', help='Delete the specified branch from all remotes.')

    args = parser.parse_args()

    # u'初始化变量'
    target_branch = args.branch
    baseline = None
    model_ext = None
    is_delete_operation = args.delete

    # u'1. 验证配置文件'
    logger.info(u"Validating configuration file: {}".format(CONFIG_FILE))
    if not validate_build_yaml(CONFIG_FILE):
        logger.error(u"Configuration validation failed. Please check '{}'. Exiting.".format(CONFIG_FILE))
        sys.exit(1)
    logger.info(u"Configuration validation successful.")

    # u'2. 确定目标分支名和相关信息'
    if not target_branch:
        # u'如果命令行未提供分支名，则从 YAML 文件解析'
        logger.info(u"Branch name not provided via argument, parsing from {}...".format(CONFIG_FILE))
        target_branch, baseline, model_ext = parse_build_yaml(CONFIG_FILE)
        if not target_branch:
            logger.error(u"Failed to derive branch name from {}. Please provide a branch name argument or fix the configuration file. Exiting.".format(CONFIG_FILE))
            sys.exit(1)
        # u'如果从 YAML 获取分支，默认是推送操作，除非显式指定了 --delete'
        if not is_delete_operation:
             logger.info(u"Defaulting to PUSH operation for branch derived from YAML.")
             # u'args.push 在这里可以不用设置，逻辑后面会处理'
        else:
             logger.info(u"DELETE operation specified for branch derived from YAML.")

    else:
        # u'如果命令行提供了分支名'
        logger.info(u"Using branch name provided via argument: '{}'".format(target_branch))
        if not is_delete_operation and not args.push:
             # u'如果提供了分支名，但没有指定 --push 或 --delete，需要明确'
             logger.warning(u"Operation type (--push or --delete) not specified for branch '{}'. Defaulting to PUSH.".format(target_branch))
             # parser.error("Please specify --push or --delete when providing a branch name.") # u'或者强制要求指定'
             # sys.exit(1)
        elif args.push:
             logger.info(u"PUSH operation specified for branch '{}'.".format(target_branch))
        elif is_delete_operation:
             logger.info(u"DELETE operation specified for branch '{}'.".format(target_branch))

    # u'3. 获取 Repo 根目录'
    logger.info(u"Determining repository root directory...")
    repo_root = get_repo_root_path_from_yaml(CONFIG_FILE)
    if not repo_root:
        logger.error(u"Failed to determine a valid repository root directory. Exiting.")
        sys.exit(1)
    logger.info(u"Using repository root: {}".format(repo_root))

    # u'4. 生成 Repo 指南 (仅在推送操作且信息完整时)'
    if not is_delete_operation:
        if baseline and model_ext:
            logger.info(u"Generating repo usage guide...")
            create_repo_guide(target_branch, baseline, model_ext, GUIDE_FILE)
        else:
            logger.warning(u"Skipping repo guide generation because baseline or external model name is missing (likely because branch name was provided via argument).")
    else:
        logger.info(u"Skipping repo guide generation during delete operation.")

    # u'5. 获取所有子仓库路径'
    logger.info(u"Listing all repositories...")
    repo_paths = get_all_repo_paths(repo_root)
    if not repo_paths:
        logger.error(u"No repositories found or failed to list them. Exiting.")
        sys.exit(1)

    # u'6. 对每个仓库执行操作'
    operation_desc = "Deletion" if is_delete_operation else "Push"
    logger.info(u"\n=== Starting Branch {} ===".format(operation_desc))
    logger.info(u"Target branch: {}".format(target_branch))
    logger.info(u"Operation: {}".format(operation_desc))
    logger.info(u"Target repositories: {}".format(len(repo_paths)))
    logger.info(u"Max retries per repository: {}".format(DEFAULT_MAX_RETRIES))
    logger.info(u"Retry delay: {} seconds".format(DEFAULT_RETRY_DELAY))
    logger.info(u"=============================\n")

    failed_repos = []
    skipped_repos = []
    successful_repos = 0

    # u'主循环处理所有仓库'
    total_repos = len(repo_paths)
    for i, repo_path in enumerate(repo_paths):
        logger.info(u"---> Processing repository {}/{} : {}".format(i + 1, total_repos, os.path.basename(repo_path)))
        # u'注意：manage_remote_branch_with_retry 的重试逻辑在其内部处理'
        success, skipped = manage_remote_branch_with_retry(
            repo_path,
            target_branch,
            delete=is_delete_operation,
            max_retries=DEFAULT_MAX_RETRIES,
            retry_delay=DEFAULT_RETRY_DELAY
        )
        if not success:
            # u'即使经过内部重试仍失败的仓库'
            failed_repos.append(os.path.basename(repo_path)) # u'记录相对路径或名称可能更清晰'
            logger.error(u"Operation FAILED for {}".format(repo_path))
        elif skipped:
            # u'操作被跳过（例如删除不存在的分支）'
            skipped_repos.append(os.path.basename(repo_path))
            logger.info(u"Operation SKIPPED for {} (branch likely didn't exist for delete)".format(repo_path))
            successful_repos += 1 # u'跳过也算作“未失败”'
        else:
            # u'操作成功'
            successful_repos += 1
            logger.info(u"Operation SUCCEEDED for {}".format(repo_path))
        logger.info(u"--- Finished processing {} ---\n".format(os.path.basename(repo_path)))


    # u'7. 打印操作总结'
    logger.info(u"\n=== Operation Summary ===")
    logger.info(u"Operation Type: {}".format(operation_desc))
    logger.info(u"Target Branch: {}".format(target_branch))
    logger.info(u"Total repositories processed: {}".format(total_repos))
    logger.info(u"Successful operations (including skips): {}".format(successful_repos))

    if skipped_repos:
        logger.info(u"Skipped repositories (e.g., branch did not exist for delete): {} repositories".format(len(skipped_repos)))
        # u'只打印前几个跳过的仓库以避免日志过长'
        display_limit = 10
        for i, repo in enumerate(skipped_repos):
            if i < display_limit:
                logger.info(u"  - {}".format(repo))
            elif i == display_limit:
                logger.info(u"  ... (and {} more)".format(len(skipped_repos) - display_limit))
                break

    if failed_repos:
        logger.error(u"Failed operations: {} repositories".format(len(failed_repos)))
        for repo in failed_repos:
            logger.error(u"  - {}".format(repo))
        logger.error(u"Please check the logs above for details on failures.")
        logger.info(u"==========================")
        sys.exit(1)  # u'如果有失败的仓库，以非零状态码退出'
    else:
        logger.info(u"All operations completed successfully (or were skipped appropriately).")
        logger.info(u"==========================")
        sys.exit(0) # u'所有操作成功完成'


if __name__ == '__main__':
    main()