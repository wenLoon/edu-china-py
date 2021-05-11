import requests  # 想要爬必须引
import json
import urllib as UrlUtils
from bs4 import BeautifulSoup
import auto_img

base_url = "http://www.tiyan.org.cn/"
url = "http://www.tiyan.org.cn/yanxuezixun.html?page=1"

# 其他请求头参数
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# 让服务器认为你是通过浏览器访问页面
page = requests.get(url=url, headers=headers)
# 转json
# json = json.loads(page.text)
soup = BeautifulSoup(page.text, 'lxml')
items = soup.find(attrs={'class': 'pic4'}).contents
res_list = []
source = ""


def judgeStr(e):
    if isinstance(e, str):
        return True
    else:
        return False


def sectionReverse(contt):
    if(len(contt.contents) == 0):
        return ""
    tagname = contt.contents[0].name
    if(tagname == "section" or len(contt.contents) != 0 and judgeStr(contt.contents[0]) == False):
        return sectionReverse(contt.contents[0])
        # print(sectionReverse(contt.contents[0]))
    else:
        return contt


def requ(href):
    # 让服务器认为你是通过浏览器访问页面
    page = requests.get(url=href, headers=headers)
    # 转json
    # json = json.loads(page.text)
    soup = BeautifulSoup(page.text, 'lxml')
    soup_pre = soup.prettify()  # 格式化输出全部内容
    # items 是一个 <listiterator object at 0x10a4b9950> 对象，不是一个list，但是可以循环遍历所有子节点。
    items = soup.find(attrs={'class': 'con'})
    constent_list = []
    for item in items.contents:
        content_obj = {}
        if item == '\n' or item == ' ' or len(item.contents) == 0:
            continue
        for i in item.contents:
            if(isinstance(item.contents[0], str)):  # 判断类型
                continue
                """ if(item.name =="h2" or item.attrs['class'][0]=="info2"):
                    continue
                content_obj["type"] = item.name
                content_obj['content'] = item.contents[0]
                constent_list.append(content_obj) """
            else:
                tagname = item.contents[0].name
                if(tagname == "img"):
                    content_obj["type"] = item.contents[0].name
                    img_src_url = item.contents[0].attrs['src']
                    content_obj['content'] = auto_img.auto_img_option(img_src_url, "tiyan_cont_")
                    constent_list.append(content_obj)
                if(tagname == "strong"):
                    content_obj["type"] = item.contents[0].name
                    content_obj['content'] = item.contents[0].contents[0]
                    constent_list.append(content_obj)
                if(tagname == "section"):
                    reve = sectionReverse(item)
                    if len(reve) > 0 and len(reve.contents) != 0:
                        if isinstance(reve.contents[0], str):  # section 来源
                            source = reve.contents[0]
                        elif len(reve.contents[0].contents) == 0:
                            continue
                        else:
                            content_obj["type"] = reve.contents[0].name
                            content_obj['content'] = reve.contents[0].contents[0]
                            constent_list.append(content_obj)

    return constent_list


def resultlist():
    for item in items:
        if item == '\n':
            continue
        img_src_source = item.contents[1].contents[0].contents[0].attrs['src']
        if(img_src_source == ""):
            img_src = img_src_source
        else:
            img_src_url = base_url + img_src_source
            img_src = auto_img.auto_img_option(img_src_url, "tiyan_cover_")
        title = item.contents[3].contents[0].contents[0]
        time = item.contents[7].contents[0]
        href = base_url + item.contents[3].contents[0].attrs['href']
        content = requ(href)
        content_str = ','.join(str(i) for i in content)
        source_src = "中国研学旅行网 "
        url = href
        if(content_str == ''):
            continue
        res_list.append([title, img_src, time, content_str, source_src, url])
    return res_list
