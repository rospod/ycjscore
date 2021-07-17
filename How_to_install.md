# 如何使用脚本
## 1.安装
1.首先下载python 3.8（不确定更高或更低版本是否可行，反正我用的是python3.8） 
[下载地址](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)  
2.安装python3.8  
双击安装，一路next
3.设置环境变量  
[参照](https://support.shotgunsoftware.com/hc/zh-cn/articles/114094235653)  
注意：
若是为自己安装  
在用户变量下的Path添加C:\Users\*\AppData\Local\Programs\Python\Python38\Scripts\和C:\Users\*\AppData\Local\Programs\Python\Python38\  
若是为所有用户安装  
在系统变量下的Path添加C:\Program Files\Python\Python38\Scripts\和C:\Program Files\Python\Python38\  
## 2.安装依赖
打开cmd或powershell    
输入
pip3 install requests  
pip3 install json  

## 3.运行  
在下载目录的根目录下（即有score.py的目录下，按住Shift右键，点击在命令提示符/PowerShell中输入  
python score.py  
按提示操作即可
