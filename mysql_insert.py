import tiyan_yanxuezixun as tyyx
import yxlx
import szjyyjy_offical_account as szjy
import pymysql
import sougou_weixin_szjyyjy as sougouwx
import json

splice_batch_sql = []
select_title = []
is_delete= 1

def transformData(source_str):
    source_str = source_str.replace("}{", "},{")
    source_str = source_str.replace("'", '\"')
    source_str = '['+ source_str +']'
    source_str = source_str.replace('\\u3000', '').replace('\\xa0', '')
    source_str = source_str.replace('\\', '')
    source_str = json.dumps(source_str, ensure_ascii=False)
    return source_str

def my_main_option():
    res = select_db()
    yxlx_option(res)
    tiyan_option(res)
    # szjyyjy_option(res)
    sougouwx_option(res)
    # 存入数据库
    if(len(splice_batch_sql) != 0):
        print("存入数据库")
        db_option()


def sougouwx_option(res):  # 三、 素质教育研究院公众号
    spider_res = sougouwx.resultlist()
    if(isinstance(spider_res, str)):
        print("需要更新key")
        return

    for item in spider_res:
        # 判断是否已经爬取
        if(item[0] in res):
            continue
        content_str = transformData(item[3])
        splice_batch_sql.append(
            (item[0], item[2], item[4], content_str, item[5], item[1], is_delete))


def szjyyjy_option(res):  # 三、 素质教育研究院公众号
    spider_res = szjy.resultlist()
    if(isinstance(spider_res, str)):
        print("需要更新key")
        return

    for item in spider_res:
        # 判断是否已经爬取
        if(item[0] in res):
            continue
        content_str = transformData(item[3])
        splice_batch_sql.append(
            (item[0], item[2], item[4], content_str, item[5], item[1], is_delete))


def tiyan_option(res):  # 中国研学网
    spider_res = tyyx.resultlist()

    for item in spider_res:
        # 判断是否已经爬取
        if(item[0] in res):
            continue
        content_str = transformData(item[3])
        splice_batch_sql.append(
            (item[0], item[2], item[4], content_str, item[5], item[1], is_delete))


def yxlx_option(res):  # 研学旅行网
    spider_res = yxlx.resultlist()

    for item in spider_res:
        # 判断是否已经爬取
        if(item[0] in res):
            continue
        content_str = transformData(item[3])
        splice_batch_sql.append(
            (item[0], item[2], item[4], content_str, item[5], item[1], is_delete))


def select_db():
    # 打开数据库连接host="localhost", user="root", password="root", database="yt", charset="utf8"
    conn = pymysql.connect(host='120.79.158.68',
                           user="root", passwd="xsdyh1234!@#$")
    conn.select_db('cceu')
    # 获取游标
    cur = conn.cursor()
    # SQL 查询语句
    sql = "SELECT title from eu_news ORDER BY publish_time DESC"
    select_title = []
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 获取所有记录列表
        results = cur.fetchall()
        if len(results) != 0:
            for row in results:
                select_title.append(row[0])
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    conn.close()
    return select_title


def db_option():
    # 打开数据库连接host="localhost", user="root", password="root", database="yt", charset="utf8"
    conn = pymysql.connect(host='120.79.158.68',
                           user="root", passwd="xsdyh1234!@#$")
    conn.select_db('cceu')
    # 获取游标
    cur = conn.cursor()

    # 另一种插入数据的方式，通过字符串传入值
    sql = "insert into eu_news(title,publish_time,source,detail,url,cover_url,is_delete) values(%s,%s,%s,%s,%s,%s,%s)"
    # [('wen', '2020-02-02', 'wen', 'spider_res[0][3]', 'wen',"", 0)]
    insert = cur.executemany(sql, splice_batch_sql)
    print('批量插入返回受影响的行数：', insert)
    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')


# my_main_option()
