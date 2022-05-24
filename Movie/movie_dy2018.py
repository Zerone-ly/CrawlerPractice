#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import bs4
import re
import win32com
from win32com.client import Dispatch, constants

thunder = win32com.client.Dispatch('ThunderAgent.Agent64.1')

cotent = []


def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    try:
        r = requests.get(url, headers=headers, timeout=5 * 60)
        r.encoding = 'gb18030'
        r.raise_for_status()
        return r.text

    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parse_data(html):
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    bsobj.encode = 'gb18030'
    # 获取电影列表
    tbList = bsobj.find_all('table', attrs={'class': 'tbspan'})

    # 对电影列表中的每一部电影单独处理
    for item in tbList:
        link = item.b.find_all('a')[1]
        # 获取电影的名称

        name = link["title"]
        url = 'https://www.dy2018.com' + link["href"]

        try:
            # 查找电影下载的磁力链接
            temp = bs4.BeautifulSoup(get_data(url), 'html.parser')
            temp.encode = 'gb18030'
            tbody = temp.find_all('tbody')

            for i in tbody:
                download = i.a.text
                if 'magnet:?xt=urn:btih' in download:
                    name = re.findall('(《.*?》)', name)[0]
                    name = name.replace('《', '').replace('》', '')

                    # thunder.AddTask(download, name, "E://Download/电影天堂/")
                    # thunder.CommitTasks()

                    print(name + "," + url + "," + download)
                    save_data(name + "," + url + "," + download)
                    break
        except Exception as e:
            print(e)


def save_data(data):
    filename = 'E://Download/电影天堂/'

    if not os.path.exists(filename):
        os.mkdir(filename)

    filename += '动作片.txt'
    with open(filename, 'a') as f:
        f.write(data + '\n')


def main():
    contents = read_config("E://Download/movieInfo.txt")
    print(contents[0])
    # 循环爬取多页数据
    # for page in range(2, 15):
    #     print('----------------------------正在爬取：第' + str(page) + '页......')
    #     # 根据之前分析的 URL 的组成结构，构造新的 url
    #     if page == 1:
    #         index = 'index'
    #     else:
    #         index = 'index_' + str(page)
    #     url = 'https://www.dy2018.com/2/' + index + '.html'
    #     # 依次调用网络请求函数，网页解析函数，数据存储函数，爬取并保存该页数据
    #     html = get_data(url)
    #     movies = parse_data(html)
    #     time.sleep(300)
    #     # save_data(movies)

    #     print('------------------------------第' + str(page) + '页完成！')


def read_config(sourcepath):
    f = open(sourcepath, encoding="utf-8")
    con = []
    lines = f.readlines()
    f.close()
    for line in lines:
        row = line.split(',')
        info = []
        for attr in row: info.append(attr)
        con.append(info)
    return con


if __name__ == '__main__':
    print('爬虫启动成功！')
    main()
    print('爬虫执行完毕！')
