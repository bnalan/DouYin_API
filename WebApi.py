# coding=utf-8
from logging import exception
import re
import json
import urllib.parse
import requests
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/DYApi")
def compute():
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        
        defurl = request.args.get("url")
        
        # 提取粘贴文字中的网址
        math1 = r'(http|ftp|https)://[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
        # 提取视频/图片Code
        math2 = r'(?<=video/)[^/]+(?=/\?|\?)'
        # 提取视频编码后的JSON
        math3 = r'(?<=json">)(.+?)(?=</script>)'

        #从共享表单或抖音复制的连接中提取网址1
        mathresult1 = re.search(math1, defurl)
        defurl1 = mathresult1.group()
        repose1 = requests.get(defurl1)

        # 获取网址1跳转后的网址，并提取此视频Code
        defurl2 = repose1.url
        mathresult2 = re.search(math2,defurl2)
        defcode = mathresult2.group()

        # 将视频/图片的Code,调用API获取返回JSON数据
        defurl3 = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + defcode
        repose2 = requests.get(defurl3,headers=header)
        dataresulr = repose2.json()

        # 判断返回值中是否含有images,即是视频下载还是图片下载
        imagedata = dataresulr['item_list'][0]['images']
        if imagedata is None:
            #下载视频
            # 请求视频网站，获取网页数据
            defurl4 = 'https://www.douyin.com/video/'+ defcode + '?previous_page=app_code_link'
            repose3 = requests.get(defurl4,headers=header)
            mathresult3 = re.search(math3,repose3.text)
            jsresult = mathresult3.group()

            # 对网页中数据进行解码，获取到视频数据的JSON
            jsresult1 = json.loads(urllib.parse.unquote(jsresult))
            trueurl = jsresult1['C_16']['aweme']['detail']['video']['playAddr']
            # API返回视频地址
            trueurl = []
            trueurl.append("http:"+trueurl[0]['src'])
            return jsonify(Result=True,Message="",Data=trueurl)
        else:
            #下载图片
            # 遍历images中的数据，添加到集合中并返回
            trueurl = []
            for data in imagedata:
                trueurl.append(data['url_list'][0])
            return jsonify(Result=True,Message="",Data=trueurl)
    except Exception as e:
        #异常捕获
        return jsonify(Result=False,Message=str(e),Data=None)
if  __name__  ==  '__main__':
    # 启动WebApi服务
    app.run(host="0.0.0.0",port=5000)