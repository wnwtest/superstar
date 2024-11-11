## repo使用工具

## build_push_script
 推荐使用build.yaml 配置branch参数 然后进行push 来新建branch 同时生成repo_guide 文档 
 ## create_repo.py
  通过对已有git文件的复制  建立新的repo 
  ```python
      # 创建参数解析器
    parser = argparse.ArgumentParser(description='根据manifest创建Git仓库')
    
    # 添加必需的命令行参数
    parser.add_argument('-m', '--manifest', 
                        type=validate_path, 
                        required=True, 
                        help='manifest.xml文件路径')
    parser.add_argument('-d', '--demo', 
                        type=validate_path, 
                        required=True, 
                        help='demo.git模板路径')
    parser.add_argument('-o', '--output', 
                        type=str, 
                        required=True, 
                        help='输出目录')

```
## manifest_simplifier
对高通基线源码的manifest的进一步处理
config.yaml文件中配置了 project name 与path的处理
进一步生成了 linkfile的汇聚文件
```yaml
operations:
  - file: "LA.VENDOR.14.3.1.r1.xml"
    name_prefix: "Mannar.LA.2.5.1/LA.VENDOR.14.3.1.r1/"
    path_prefix: "LA.VENDOR.14.3.1.r1/LINUX/android/"
  - file: "KERNEL.PLATFORM.3.0.r6.xml"
    name_prefix: "Mannar.LA.2.5.1/LA.VENDOR.14.3.1.r1/"
    path_prefix: "LA.VENDOR.14.3.1.r1/LINUX/android/"
  - file: "LA.QSSI.14.0.r1.xml"
    name_prefix: "Mannar.LA.2.5.1/LA.QSSI.14.0.r1/"
    path_prefix: "LA.VENDOR.14.3.1.r1/LINUX/android/"
  - file: "LA.QSSI.15.0.xml"
    name_prefix: "Mannar.LA.2.5.1/LA.QSSI.15.0/"
    path_prefix: "LA.QSSI.15.0/LINUX/android/"
```
## others
其他的是一些基于具体需求产生的程序  可参考  具体怎么用已经不记得了
