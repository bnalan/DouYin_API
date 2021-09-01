# 抖音无水印WebApi服务端

利用Python3，将请求参数转换为需要提取的无水印视频/图片直链，配合IOS捷径可快速下载。

***
* 服务端部署
1. 安装python环境
2. 安装flask,requests包
3. 运行`WebApi.py`
***
### 1. 安装Python依赖包
```
    pip install requests==2.20.0   
    pip install flask
```

### 2. 运行 `WebApi.py`
##### &emsp;如部署到服务器上，可用nohup后台运行此脚本。
```
    nohup python robot.py &
```
### 3、请求参数
```
    http://localhost(服务器IP):5000/DYApi?url="复制的抖音链接"
```
### 4、返回参数
* Result(bool)：处理结果
* Data(List<string>)：视频/图片的直链
* Message(string):错误信息
```json
    {"Data":"视频/图片直链","Message":"","Result":true}
```
### 5、在IOS中捷径的用法
![IOS捷径](https://github.com/bnalan/DouYin_API/tree/master/image/jiejing.jpg)