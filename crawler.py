import json
import requests
from bs4 import BeautifulSoup as BS
import time
import pandas as pd


def region_play_cnt():
    url_dict = {
        '全站': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all',
        '番剧': 'https://api.bilibili.com/pgc/web/rank/list?day=3&season_type=1',
        '动画': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=1&type=all',
        '音乐': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=3&type=all',
        '舞蹈': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=129&type=all',
        '游戏': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=4&type=all',
        '知识': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all',
        '科技': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all',
        '运动': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=234&type=all',
        '汽车': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=223&type=all',
        '生活': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=160&type=all',
        '美食': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=211&type=all',
        '动物圈': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=217&type=all',
        '鬼畜': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=119&type=all',
        '时尚': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=155&type=all',
        '娱乐': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=5&type=all',
        '影视': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=181&type=all',
        '原创': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=origin',
        '新人': 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.bilibili.com',
        'Host': 'api.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15',
        'Accept-Language': 'zh-cn',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bilibili.com/v/popular/rank/all'
    }

    for i in url_dict.items():
        url = i[1]
        tab_name = i[0]
        title_list = []
        play_cnt_list = []
        try:
            r = requests.get(url, headers=headers)
            json_data = r.json()
            list_data = json_data['data']['list']
            for data in list_data:
                title_list.append(data['title'])
                play_cnt_list.append(data['stat']['view'])
        except Exception as e:
            print("爬取失败:{}".format(str(e)))

        df = pd.DataFrame(
            {
                '视频标题': title_list,
                '播放数': play_cnt_list,
             }
        )
        df.to_csv('./result/crawl_result/region_play/{}.csv'.format(tab_name), encoding='utf_8_sig')


def region_tag():
    url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=231&page={}&pagesize=20&jsonp=jsonp&time_from=20231109&time_to=20231116'
    page = 20
    tags = []
    for i in range(0, page):
        url = url.format(i)
        try:
            response = requests.get(url, timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
        result = json.loads(response.text)
        items = result['result']
        for item in items:
            tags.append(item['tag'])
    df = pd.DataFrame(
        {
            '标签': tags
        }
    )
    df.to_csv('./result/crawl_result/region_tag/科技.csv', encoding='utf_8_sig')


def video_danmu():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)", }
    r1 = requests.get(url='https://api.bilibili.com/x/player/pagelist?bvid=BV1bH4y1B7zk', headers=headers)
    html1 = r1.json()
    cid = html1['data'][0]['cid']
    danmu_url = 'http://comment.bilibili.com/{}.xml'.format(cid)
    r2 = requests.get(danmu_url)
    soup = BS(r2.content, 'xml')
    danmu_list = soup.find_all('d')
    time_list = []
    text_list = []
    for d in danmu_list:
        data_split = d['p'].split(',')
        temp_time = time.localtime(int(data_split[4]))
        danmu_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
        time_list.append(danmu_time)
        text_list.append(d.text)
        print('{}:{}'.format(danmu_time, d.text))
    df = pd.DataFrame(
        {
            '时间': time_list,
            '弹幕': text_list
        }
    )
    df.to_csv('./result/crawl_result/video_danmu/弹幕.csv', encoding='utf_8_sig')


if __name__ == "__main__":
    region_play_cnt()
    region_tag()
    video_danmu()