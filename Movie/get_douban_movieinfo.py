import json
from random import randint
import time
import bs4 as bs4
import requests
import os

douban_url = 'https://movie.douban.com/typerank?'
typename_list = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '情色']
type_list = [11, 24, 5, 13, 17, 25, 10, 19, 20, 6]
interval_list = ['100:90', '90:80', '80:70', '70:65']
type_idx = 0
interval_idx = 0


def get_page_html(url, params):
    headers = {
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36 '
    }
    try:
        response = requests.get(url, headers=headers, timeout=30, params=params)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None


def get_page_data(html):
    ans = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup.encode = 'gb18030'
    items = json.loads(repr(soup))['subjects']
    for item in items:
        info = item['title'] + ',' + item['rate'] + ',' + item['url']
        print(info)
        save_data(info)
    return ans


def get_movie_info(html, typename):
    ans = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    soup.encode = 'utf-8'
    items = json.loads(repr(soup))
    for item in items:
        regions = repr(item['regions']).replace('[', '').replace(']', '').replace(',', '|')
        info = item['id'] + ',' + typename + ',' + item['title'] + ',' + regions + ',' + item['score'] + ',' + item[
            'release_date'] + ',' + item['url'] + ',' + item['cover_url']
        print(info)
        save_data(info)
    return ans


def save_data(data):
    filename = 'E://Download/'

    if not os.path.exists(filename):
        os.mkdir(filename)

    filename += 'movieInfo.txt'
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(data + '\n')


def main():
    typeIdx = 1
    intervalIdx = 0
    idx_page = 0

    url = 'https://movie.douban.com/j/chart/top_list?'

    while typeIdx < len(type_list):

        if intervalIdx >= len(interval_list):
            typeIdx += 1
            idx_page = 0
            intervalIdx = 0

        mainType = type_list[typeIdx]
        interval_id = interval_list[intervalIdx]

        print(typename_list[typeIdx] + ',' + interval_id + '---------------------------------------正在爬取：第' + str(
            idx_page + 1) + '页......')

        params = {"type": mainType, "interval_id": interval_id, "action": "", "start": idx_page * 20, "limit": 20}
        html = get_page_html(url, params)
        if len(html) <= 2:
            intervalIdx += 1
            idx_page = 0
        else:
            get_movie_info(html, typename_list[typeIdx])
            idx_page += 1
        rad = randint(1, 5)
        time.sleep(rad)
        print(typename_list[typeIdx] + ',' + interval_id + '---------------------------------------第' + str(
            idx_page + 1) + '页完成！')
        print('\n')


if __name__ == '__main__':
    print('爬虫启动成功！')
    main()
    print('爬虫执行完毕！')
