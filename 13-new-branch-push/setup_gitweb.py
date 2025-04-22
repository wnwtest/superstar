# -*- coding: utf-8 -*-
# wang nanwang 2024
import os
import sys
import re
import subprocess


# 全局服务器地址配置
SERVER_IP = "192.168.117.71"


class GitWebSetup:
    def __init__(self, project_name):
        self.project_name = project_name
        self.www_path = "/var/www"
        self.apache_ports_conf = "/etc/apache2/ports.conf"
        self.apache_default_conf = "/etc/apache2/sites-available/000-default.conf"


    def find_next_available_port(self):
        """
        查找下一个可用端口号
        通过解析ports.conf中已存在的Listen端口（兼容大小写）
        """
        try:
            with open(self.apache_ports_conf, 'r') as f:
                content = f.read()
                # 使用不区分大小写的正则匹配所有端口号
                existing_ports = re.findall(r'[Ll]isten\s+(\d+)', content)
                
                # 转换为整数并排序
                existing_ports = [int(port) for port in existing_ports]
                
                # 找出最大端口号并+1
                next_port = max(existing_ports) + 1
                
                # 检查新端口是否已存在
                while next_port in existing_ports:
                    next_port += 1
                
                return next_port
        except Exception as e:
            print("查找端口号失败: {}".format(e))
            return 8109  # 默认端口


    def add_port_to_apache_config(self, port):
        """
        安全地将端口添加到ports.conf
        确保不重复添加且正确插入
        兼容大小写的Listen
        """
        try:
            # 先检查是否已存在（不区分大小写）
            with open(self.apache_ports_conf, 'r') as f:
                content = f.read()
                if re.search(r'[Ll]isten\s+{}'.format(port), content, re.IGNORECASE):
                    print("端口 {} 已存在".format(port))
                    return
            
            # 读取文件内容
            with open(self.apache_ports_conf, 'r') as f:
                lines = f.readlines()
            
            # 找到最后一个非SSL和非注释的Listen端口行
            last_listen_index = -1
            for i in range(len(lines)):
                # 使用不区分大小写的匹配
                if re.match(r'\s*[Ll]isten\s+\d+', lines[i]) and not re.search(r'443', lines[i]):
                    last_listen_index = i
            
            # 插入新的端口（使用大写Listen）
            if last_listen_index != -1:
                lines.insert(last_listen_index + 1, "Listen {}\n".format(port))
            else:
                # 如果没找到，就在文件末尾添加
                lines.append("Listen {}\n".format(port))
            
            # 写回文件
            with open(self.apache_ports_conf, 'w') as f:
                f.writelines(lines)
            
            print("成功添加端口 {}".format(port))
        except Exception as e:
            print("添加端口失败: {}".format(e))

    def modify_apache_default_conf(self, project_name, port):
        """
        安全地修改Apache默认配置
        添加完整的VirtualHost节点
        """
        try:
            # 准备VirtualHost配置
            new_vhost = """
    <VirtualHost *:{0}>
        ServerName {1}
        DocumentRoot {2}
        ScriptAlias /{1} {2}/{1}_gitweb.cgi
    </VirtualHost>
    """.format(port, project_name, self.www_path)
            
            # 读取现有配置
            with open(self.apache_default_conf, 'r') as f:
                content = f.read()
            
            # 检查是否已存在相同的VirtualHost
            if "<VirtualHost *:{0}>".format(port) not in content:
                # 在文件末尾添加新的VirtualHost
                with open(self.apache_default_conf, 'a') as f:
                    f.write(new_vhost)
                print("成功修改Apache配置")
            else:
                print("VirtualHost配置已存在")
        except Exception as e:
            print("修改Apache配置失败: {}".format(e))
    def setup_cgi_file(self):
        """
        设置CGI文件权限并创建软链接
        如果软链接已存在则跳过
        """
        try:
            # CGI文件路径
            project_path = "/home/git/review_site/git/{}".format(self.project_name)
            cgi_filename = "{}_gitweb.cgi".format(self.project_name)
            
            # 完整路径
            cgi_full_path = os.path.join(project_path, cgi_filename)
            www_cgi_link = os.path.join(self.www_path, cgi_filename)
            
            # 修改CGI文件权限
            subprocess.call(['chmod', '777', cgi_full_path])
            
            # 创建软链接（仅当不存在时）
            if not os.path.exists(www_cgi_link):
                subprocess.call(['sudo', 'ln', '-sf', cgi_full_path, www_cgi_link])
                print("成功创建CGI文件软链接")
            else:
                print("CGI文件软链接已存在，跳过")
        except Exception as e:
            print("设置CGI文件失败: {}".format(e))

    def restart_apache(self):
        """
        重启Apache服务
        """
        try:
            subprocess.call(['sudo', '/etc/init.d/apache2', 'restart'])
            print ("Apache服务重启成功")
        except Exception as e:
            print ("重启Apache服务失败: {}".format(e) )


    def setup(self):
        """
        执行全部设置步骤
        """
        try:
            # 找到可用端口
            port = self.find_next_available_port()
            
            # 添加端口到配置
            self.add_port_to_apache_config(port)
            
            # 修改Apache默认配置
            self.modify_apache_default_conf(self.project_name, port)
            
            # 设置CGI文件
            self.setup_cgi_file()
            
            # 重启Apache
            self.restart_apache()
            
            # 输出访问地址
            print("项目 {} 配置完成".format(self.project_name))
            print("访问地址: http://{}:{}".format(SERVER_IP, port))
            print("访问路径: http://{}:{}/{}".format(SERVER_IP, port, self.project_name))
        except Exception as e:
            print("配置过程发生错误: {}".format(e))


def main():
    # 从命令行参数获取项目名
    if len(sys.argv) < 2:
        print ("请提供项目名称")
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    # 创建并执行设置
    setup = GitWebSetup(project_name)
    setup.setup()


if __name__ == '__main__':
    main()