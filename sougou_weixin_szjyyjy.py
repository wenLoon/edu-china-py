import requests  # 想要爬必须引
import json
import random
import time
import urllib as UrlUtils
from bs4 import BeautifulSoup
from urllib import request
import datetime
import auto_img 

base_url = "https://weixin.sogou.com"
url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%B4%A0%E8%B4%A8%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6%E9%99%A2&ie=utf8&_sug_=n&_sug_type_="

# 其他请求头参数
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)",
    "Connection": "keep-alive",
    "Accept": "/"
}
# 让服务器认为你是通过浏览器访问页面
page = requests.get(url=url, headers=headers, verify=False)
# 转json
# json = json.loads(page.text)
soup = BeautifulSoup(page.text, 'lxml')
# '{"base_resp":{"ret":-3,"errmsg":"no session","cookie_count":0,"csp_nonce":1501328633},"ret":-3,"errmsg":"no session","cookie_count":0}'
items = soup.find(attrs={'id': 'sogou_vr_11002301_box_0'})
item_href = soup.find(attrs={'uigs': 'account_article_0'})
item_source = items.find(attrs={'class': 'identify'}).next

res_list = []

def get_real_url(fake_url):
    real_url = fake_url[fake_url.find('url +=')+6:fake_url.find('url.replace("@"')]
    real_url = real_url.replace("url +=", "")
    real_url = real_url.replace("\r\n", "")
    real_url = real_url.replace("\'", "")
    real_url = real_url.replace(";", "")
    real_url = real_url.replace(" ", "")
    real_url = real_url.replace("@", "")
    return real_url
def judgeStr(e):
    if isinstance(e, str):
        return True
    else:
        return False


def sectionReverse(contt):
    list_contt = []
    if(contt.name == "br" or len(contt.contents) == 0):
        return
    for index in range(len(contt.contents)):
        item = contt.contents[index]
        if(isinstance(item, str)):
            content_obj = {}
            content_obj["type"] = contt.name
            content_obj['content'] = item
            list_contt.append(content_obj)
        else:
            if(item.name == "br" or len(item.contents) == 0):
                continue
            concat_temp = sectionReverse(item)
            list_contt = list_contt + concat_temp
    # if(isinstance(contt.contents, str)):
    return list_contt


def requ(href):
    # 破解搜狗加密url
    b = int(random.random() * 100) + 1
    a = href.find("url=")
    result_link = href + "&k=" + str(b) + "&h=" + href[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    a_url =result_link
    time.sleep(3)
    # 让服务器认为你是通过浏览器访问页面
    cookie_sougou = 'ABTEST=4|1619622952|v1; IPLOC=CN5101; SUID=35CCDEB7721A910A0000000060897C28; SNUID=F72329126F75B1F0172911D170CA0674; PHPSESSID=mcm2jp0n3n0415opekqbkgan46'
    headers_sougou = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Host": 'weixin.sogou.com',
        "Cookie": cookie_sougou
    }
    page = requests.get(url=a_url, headers=headers_sougou, verify=False,allow_redirects = True)
    real_url = get_real_url(page.text)
    page_redirect = requests.get(url=real_url, headers=headers, verify=False)
    # 转json
    # json = json.loads(page.text)
    soup = BeautifulSoup(page_redirect.text, 'lxml')
    items = soup.find(attrs={'class': 'rich_media_content'})
    constent_list = []
    if(items is None):
        return constent_list
    res_spider_list = items.contents[1].contents[4].contents[4:]
    if(len(res_spider_list) == 0):
        res_spider_list = items.contents[1].contents[4:]
    for item in res_spider_list:
        content_obj = {}
        if item == '\n' or item == ' ' or item.name == 'br':
            continue
        item_contents = item.contents
        for i in range(len(item_contents)):
            if(item_contents[i] == '\n' or item_contents[i] == ' ' or item_contents[i].name == 'br'):
                continue
            if(isinstance(item.contents[i], str)):  # 判断类型
                content_obj = {}
                content_obj["type"] = item.name
                content_obj['content'] = item.contents[i]
                constent_list.append(content_obj)
            else:
                if(isinstance(item.contents[i].contents, list)):
                    reve = sectionReverse(item.contents[i])  # 判断类型
                    constent_list.extend(reve)

    return constent_list


def resultlist():
    img_src_url = "https://mmbiz.qpic.cn/mmbiz_jpg/TLo8OEdyVibx4pb3W4MIE06BjWoOodiaX3ZcXb2iajJeeek2CEhbeian4mAURRzL6t0Fdy1ervKbChIDruMiaUY3laQ/0?wx_fmt=jpeg"
    img_src = auto_img.auto_img_option(img_src_url, "sougou_cover_")
    title = item_href.text[:-3]
    datetime_struct = item_href.nextSibling.next.next[28:38]
    datetime_struct = int(datetime_struct)     
    datetime_struct = datetime.datetime.fromtimestamp(datetime_struct)
    time = (datetime_struct.strftime('%Y-%m-%d'))  # 2016-12-22
    href = base_url + item_href.attrs['href']
    source_src = item_href
    content = requ(href)
    content_str = ','.join(str(i) for i in content)
    if(content_str == ''):
        return []
    res_list.append([title, img_src, time, content_str, item_source, href])
    # res_list.append([title, img_src, time, content, source_src, url])
    return res_list


