# 爬取https://www.dy2018.com电影并下载
# -*- coding: UTF-8 -*-

# pip install requests   安装网络包
# pip install bs4        安装网络解析包
# pip install pypiwin32  安装系统win32调用包
# 下载迅雷

from random import randint
import requests
import bs4
import re
import time
import os
import win32com
from win32com.client import Dispatch, constants

thunder = win32com.client.Dispatch('ThunderAgent.Agent64.1')


# 请求数据
def request_dy2018(url):
    # 伪装Header
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    try:
        r = requests.get(url, headers=headers, timeout=5 * 60)
        r.encoding = 'gb18030'
        if r.status_code == 200:
            return r.text
        return None
    except requests.RequestException:
        return None


# 解析数据
def parse_data(html):
    # 用html解析器解析数据
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # 指定编码
    soup.encode = 'gb18030'
    # 获取电影列表
    tbList = soup.find_all('table', attrs={'class': 'tbspan'})
    # 对电影列表中的每一部电影单独处理
    for item in tbList:
        # 获取电影评分
        fonts = item.find_all('font')
        if len(fonts) < 2: continue
        scorestr = item.find_all('font')[1].text
        scorestrarr = repr(scorestr).split(':')
        if len(scorestrarr) < 2: continue
        score = float(scorestrarr[1].split('  ')[0].replace(' ', ''))
        if score <= 6: continue
        # 获取电影名字
        link = item.b.find_all('a')[1]
        name = link["title"]
        # 获取详情链接
        url = 'https://www.dy2018.com' + link["href"]

        try:
            # 查找电影下载的磁力链接
            temp = bs4.BeautifulSoup(request_dy2018(url), 'html.parser')
            temp.encode = 'gb18030'
            tbody = temp.find_all('tbody')
            info = []
            for i in tbody:
                download = i.a.text
                # 查找第一个磁力链接
                if 'magnet:?xt=urn:btih' in download:
                    name = re.findall('(《.*?》)', name)[0]
                    name = name.replace('《', '').replace('》', '')
                    # 保存信息
                    print(name)
                    thunder.AddTask(download, name, "E://Download/电影天堂/")
                    thunder.CommitTasks()
                    break
        except Exception as e:
            print(e)


# def save_data(data):
#     print(data)
#     filename = 'E://Download/'

#     if os.path.exists(filename) == False:
#         os.mkdir(filename)

#     filename += 'dy2018_movie.txt'
#     with open(filename,'a',encoding='utf-8') as f:
#         f.write(data + '\n')


def get_data():
    maintype = 1
    page = 1
    while maintype < 21:
        if page == 1:
            index = 'index'
        else:
            index = 'index_' + str(page)
        # 拼接网页
        url = 'https://www.dy2018.com/' + str(maintype) + '/' + index + '.html'
        print(str(maintype) + '---------------------------------------第' + str(page) + '页开始！')
        html = request_dy2018(url)
        if html is None or len(html) <= 2:
            maintype += 1
            page = 1
        else:
            parse_data(html)
            page += 1
        # 随机时间
        rad = randint(1, 3)
        time.sleep(rad)
        print(str(maintype) + '---------------------------------------第' + str(page) + '页完成！')
        print('\n')


def main():
    get_data()


if __name__ == '__main__':
    print('爬虫启动成功！')
    main()
    print('爬虫执行完毕！')
