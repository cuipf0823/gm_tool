# 环境配置

1. 安装虚拟环境(以Debian为例);
```
sudo apt-get install python-virtualenv
```
2. 创建gm工具运行的python虚拟环境;
```
virtualenv --python=python3 gm_env
```
3. 运行虚拟环境;
```
source gm_env/bin/activate
//虚拟环境退出命令
deactivate
```
4. 安装程序目录下需求文件;
```
 pip install -r requirements
```

# 启动
直接使用start脚本即可;
