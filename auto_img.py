from bs4 import BeautifulSoup
import requests
import random
import os

# SAVE_PATH =r'D:\study\python\edu-china\img'
SAVE_PATH =r'/data/application/cceu/spider/'
# SAVE_PATH =r'/usr/local/application/cceu/python/edu-china/img/'

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
 

def auto_img_option(select_imgurl, name):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)",
        "Connection": "keep-alive",
        "Accept": "/"
    }
    if(select_imgurl == "" or ("http" not in select_imgurl)):
        return ""
    req = requests.get(select_imgurl, headers=headers, verify=False)
    name = name + str(random.randint(0,999999999))
    path = SAVE_PATH
    # mkdir(path)
    file_name = path + name+".jpg"
    f = open(file_name, 'wb')
    f.write(req.content)
    print(name)
    f.close
    return "/spider/"+name+".jpg"

# imgurl = "http://www.tiyan.org.cn//public/upload/2021/04/23/7c16251a227b790d5c375b16b1615371.jpg"
# name = "zgyx_cover_"
# auto_img_option(imgurl, name)

