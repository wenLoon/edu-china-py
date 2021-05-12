import requests  # 想要爬必须引
import json
import urllib as UrlUtils
from bs4 import BeautifulSoup
import auto_img

base_url = "https://www.yxlx.com.cn/"
url = "https://www.yxlx.com.cn/02.html?p_article_list=1"

# 其他请求头参数
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# 让服务器认为你是通过浏览器访问页面
page = requests.get(url=url, headers=headers, verify=False)
# 转json
# json = json.loads(page.text)
soup = BeautifulSoup(page.text, 'lxml')
items = soup.find(attrs={
                  'class': 'article_list-layerF9DA1AACA17D97116E00BDE208A5576F'}).contents[1].contents
res_list = []


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
    page = requests.get(url=href, headers=headers, verify=False)
    # 转json
    # json = json.loads(page.text)
    soup = BeautifulSoup(page.text, 'lxml')
    soup_pre = soup.prettify()  # 格式化输出全部内容
    # items 是一个 <listiterator object at 0x10a4b9950> 对象，不是一个list，但是可以循环遍历所有子节点。
    items = soup.find(attrs={'class': 'artview_detail'})
    source = soup.find(attrs={'class': 'org_txt'}).nextSibling
    constent_list = []
    for item in items.contents:
        content_obj = {}
        if item == '\n' or item == ' ' or item.name == 'br':
            continue
        if item.name == 'div':
            break
        item_contents = item.contents
        for i in range(len(item_contents)):
            if(item_contents[i] == '\n' or item_contents[i].name == 'br'):
                continue
            if(isinstance(item.contents[i], str)):  # 判断类型
                content_obj = {}
                content_obj["type"] = item.name
                content_obj['content'] = item.contents[i]
                constent_list.append(content_obj)
            else:
                tagname = item.contents[i].name
                if(tagname == "a"):
                    content_obj = {}
                    content_obj["type"] = item.contents[i].name
                    content_obj["href"] = item.contents[i].attrs["href"]
                    content_obj['content'] = item.contents[i].contents[0]
                    cont= str(content_obj['content'])
                    if("<" not in cont):
                        constent_list.append(content_obj)
                elif(tagname == "span"):
                    if(len(item.contents[i].contents)>0):
                        if(judgeStr(item.contents[i].contents[0]) == True):
                            content_obj = {}
                            content_obj["type"] = item.contents[i].name
                            content_obj['content'] = item.contents[i].contents[0]
                            constent_list.append(content_obj)
                        else:
                            for j in range(len(item.contents[i].contents)):
                                cont_i_j= item.contents[i].contents[j]
                                print(cont_i_j)
                                if(cont_i_j == "" or cont_i_j == "\n" or cont_i_j.name == "br"):
                                    continue
                                if(len(item.contents[i].contents[j].contents)>0):
                                    if(judgeStr(item.contents[i].contents[j].contents[0]) == True):
                                        content_obj = {}
                                        content_obj["type"] = item.contents[i].contents[j].name
                                        content_obj["content"] = item.contents[i].contents[j].contents[0]
                                        constent_list.append(content_obj)
                else:
                    if(tagname == 'div'):
                        for j in range(len(item.contents[i].contents)):
                            tagname_div = item.contents[i].contents[j].name
                            if(tagname_div == 'img'):
                                content_obj = {}
                                content_obj["type"] = item.contents[i].contents[j].name
                                img_src_url = item.contents[i].contents[j].attrs["src"]
                                content_obj['src'] = auto_img.auto_img_option(img_src_url, "yxlx_cont_")
                                constent_list.append(content_obj)

    return [source, constent_list]


def resultlist():
    for item in items:
        if item == '\n':
            continue
        img_src_url = item.contents[1].contents[3].contents[0].attrs['data-original']
        img_src = auto_img.auto_img_option(img_src_url, "yxlx_cover_")
        title = item.contents[1].contents[3].contents[0].attrs['alt']
        time = item.contents[4].contents[3].contents[0].contents[0]
        href = item.contents[1].contents[3].attrs['href']
        content = requ(href)
        content_str = ','.join(str(i) for i in content[1])
        source_src = content[0]
        url = href
        if(content_str == ''):
            continue
        res_list.append([title, img_src, time, content_str, source_src, url])
    return res_list


# resultlist()
