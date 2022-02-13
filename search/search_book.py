import argparse
import os
import re
import sys
import json

import requests

max_retry = 10

headers = {
    'User-Agent': 'boluobao/4.5.52(iOS;14.0)/appStore',
    'Host': 'api.sfacg.com',
    'Authorization': 'Basic YXBpdXNlcjozcyMxLXl0NmUqQWN2QHFlcg=='
}
NovelInfo = 'novels/{}?expand=chapterCount%2CbigBgBanner%2CbigNovelCover%2CtypeName%2Cintro%2Cfav%2Cticket' \
            '%2CpointCount%2Ctags%2CsysTags%2Csignlevel%2Cdiscount%2CdiscountExpireDate%2CtotalNeedFireMoney' \
            '%2Crankinglist%2CoriginTotalNeedFireMoney%2Cfirstchapter%2Clatestchapter%2Clatestcommentdate%2Cessaytag' \
            '%2CauditCover%2CpreOrderInfo%2CcustomTag%2Ctopic%2CunauditedCustomtag%2ChomeFlag'


def get(api_url):
    api_url = 'https://api.sfacg.com/' + api_url.replace('https://api.sfacg.com/', '')
    for i in range(max_retry):
        try:
            return requests.get(api_url, headers=headers).json()
        except (OSError, TimeoutError, IOError) as error:
            print("\nGet Error Retry: " + api_url)


def tag_(tag):
    return ', '.join([tags['tagName'] for tags in tag])


def re_novel_id(book_id: str):
    book_id = book_id if 'http' not in book_id else \
        re.findall(r'/([0-9]+)/?', book_id)[0]
    if book_id.isdigit():
        return book_id, 200
    else:
        return f'输入信息 {book_id} 不是数字！', 403


def search_book_id(novel_id: str):
    response = get(NovelInfo.format(novel_id))
    if response['status']['httpCode'] == 200:
        print('书籍名称：', response['data']['novelName'])
        print('书籍序号：', response['data']['novelId'])
        print('书籍作者：', response['data']['authorName'])
        print('书籍字数：', response['data']['charCount'])
        print('签约状态：', response['data']['signStatus'])
        print('书籍标签：', tag_(response['data']['expand']['sysTags']))
        print('最新章节：', response['data']['expand']['latestChapter']['title'],
              '\t章节序号:', response['data']['expand']['latestChapter']['chapId'])
        print('更新时间：', response['data']['lastUpdateTime'])
        print('全订价格：', response['data']['expand']['originTotalNeedFireMoney'])

    else:
        print(response['status']['msg'])


def search_json(novel_id, code):
    http_mode = True if not os.path.exists("bookInfo.json") else False
    if http_mode:
        search_book_id(novel_id)
        return
    if code != 200:
        print(novel_id)
    else:
        read_json = open('bookInfo.json', 'r', encoding='utf-8').read()
        book_info = json.loads(read_json)['BOOKID'][str(novel_id)]
        print('书籍名称：', book_info['novelName'])
        print('书籍序号：', book_info['novelId'])
        print('书籍作者：', book_info['authorName'])
        print('书籍字数：', book_info['charCount'])
        print('签约状态：', book_info['signStatus'])
        print('书籍标签：', tag_(book_info['expand']['sysTags']))
        print('最新章节：', book_info['expand']['latestChapter']['title'],
              '\t章节序号:', book_info['expand']['latestChapter']['chapId'])
        print('更新时间：', book_info['lastUpdateTime'])
        print('全订价格：', book_info['expand']['originTotalNeedFireMoney'])


def main():
    print('数据更新时间 2022-01-22')
    parser = argparse.ArgumentParser()
    parser.add_argument("book_id", help="please input the [novel id] or [novel url]")
    args = parser.parse_args()
    book_id = args.book_id
    try:
        search_json(*re_novel_id(book_id))
    except KeyError:
        print('搜索信息不存在')


if __name__ == '__main__':
    main()
