import requests  # 想要爬必须引
import json
import urllib as UrlUtils
from bs4 import BeautifulSoup
import datetime
import auto_img

base_url = "https://www.yxlx.com.cn/"
url = "https://mp.weixin.qq.com/mp/profile_ext"

# 其他请求头参数
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1326.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)",
    "Connection": "keep-alive",
    "Accept": "/"
}
offset = "0"
key = "c210791e4f10c22e19ffb4a4137bc5bb354a30a3a883303c3d919d0e18278d54a0cb722c24c5331a84665ddb94fcce9b3c0774eb2db32743925e5264b1b35312c10509dbf3fda3b8fd59a1a412fe9f2a1902f27d21b9fe2859538397f101ce1549795ba61a7d5bfe29046728d3a59599f9e2b1e0a903f45002001707b967cd3e"
# 参数
params = {
    "action": "getmsg",
    "__biz": "Mzg2MDUxODQ5Mw==",
    "f": "json",
    "offset": offset,
    "count": "10",
    "is_ok": "1",
    "scene": "124",
    "uin": "MTc4MTA2MzQxMw==",
    "key": key,
    "pass_ticket": "wyCJO4HAVlD%2B95pCqEK38VhHo%2BDoNFeba43Qwxje6lvEoirO9gYPjcS%2FbMn9cUZy",
    "wxtoken": "",
    "appmsg_token": "1110_dSEYqS5ef1lwrgmGrgJxO_MUc0vH2L5yqsI9pA~~",
    "x5": "0",
    "f": "json"
}
# 让服务器认为你是通过浏览器访问页面
page = requests.get(url=url, headers=headers, params=params, verify=False)
# 转json
# json = json.loads(page.text)
soup = BeautifulSoup(page.text, 'lxml')
# '{"base_resp":{"ret":-3,"errmsg":"no session","cookie_count":0,"csp_nonce":1501328633},"ret":-3,"errmsg":"no session","cookie_count":0}'
items = soup.contents[0].contents[0].contents[0].contents[0]
no_session = '"errmsg":"no session"'

res_list = []


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
    # 让服务器认为你是通过浏览器访问页面
    page = requests.get(url=href, headers=headers, verify=False)
    # 转json
    # json = json.loads(page.text)
    soup = BeautifulSoup(page.text, 'lxml')
    items = soup.find(attrs={'class': 'rich_media_content'})
    no_session = '"errmsg":"no session"'
    constent_list = []
    if(items is None):
        return constent_list
    if(no_session in items):
        return print("需要更新key")
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
    if(no_session in items):
        return "need update key"
    general_msg_list = eval(items)
    temp_list = general_msg_list['general_msg_list']
    res_spider_list = eval(temp_list)
    for item in res_spider_list['list']:
        item_app_msg_ext_info = item["app_msg_ext_info"]
        item_comm_msg_info = item["comm_msg_info"]
        img_src_url = item_app_msg_ext_info['cover'].replace(
            "\\", "").replace("http", "https")
        img_src = auto_img.auto_img_option(img_src_url, "szjyyjy_cover_")
        title = item_app_msg_ext_info['title']
        # 时间戳
        datetime_struct = item_comm_msg_info["datetime"]
        datetime_struct = datetime.datetime.fromtimestamp(datetime_struct)
        time = (datetime_struct.strftime('%Y-%m-%d'))  # 2016-12-22
        href = item_app_msg_ext_info['content_url'].replace(
            "\\", "").replace("http", "https")
        source_src = item_app_msg_ext_info["author"]
        url = href
        content = requ(href)
        content_str = ','.join(str(i) for i in content)
        if(content_str == ''):
            continue
        res_list.append([title, img_src, time, content_str, source_src, url])
    return res_list
