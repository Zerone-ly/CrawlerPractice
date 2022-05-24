#!/usr/bin/python
# -*- coding: UTF-8 -*-

from fileinput import filename
import os
import requests
import bs4
import re
import pandas as pd


def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    try:
        r = requests.get(url, headers=headers)
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
    bsobj.encode= 'gb18030'
    info = []
    # 获取电影列表
    tbList = bsobj.find_all('table', attrs={'class': 'span'})

    # print(bsobj)

    # 对电影列表中的每一部电影单独处理
    for item in tbList:
        movie = []
        link = item.b.find_all('a')[1]
        # 获取电影的名称
        # print(link)
        name =link["title"]
        url = 'https://www.66yingshi.com' + link["href"]
        print(name)

        try:
            # 查找电影下载的磁力链接
            temp = bs4.BeautifulSoup(get_data(url),'html.parser')
            temp.encode =  'gb18030'
            tbody = temp.find_all('tbody')
            
            for i in tbody:
                download = i.a.text
                if 'magnet:?xt=urn:btih' in download:
                    movie.append(name)
                    movie.append(url)
                    movie.append(download)
                    #print(movie)
                    info.append(movie)
                    break
        except Exception as e:
            print(e)
      

    return info


def save_data(data):
    filename = 'E://Download/蛋蛋赞/'

    if os.path.exists(filename) == False:
        os.mkdir(filename)
    
    filename += '动作片.csv'

    print(filename)

    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)


def main():
    # 循环爬取多页数据
    for page in range(2, 3):
        print('正在爬取：第' + str(page) + '页......')
        # 根据之前分析的 URL 的组成结构，构造新的 url
        if page == 1:
            index = 'index'
        else:
            index = 'index_' + str(page)
        url = 'https://www.66yingshi.com/xijupian/' + index + '.html'
        # 依次调用网络请求函数，网页解析函数，数据存储函数，爬取并保存该页数据
     
        # print(url)
        html = get_data(url)
        # print(html)
        movies = parse_data(html)
        # save_data(movies)

        print('第' + str(page) + '页完成！')


if __name__ == '__main__':
    print('爬虫启动成功！')
    main()
    print('爬虫执行完毕！')
