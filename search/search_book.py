import click
import os
import re
import sys
import json
import headers


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
    response = headers.get(headers.json_info["NovelInfo"].format(novel_id))
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


def bookshelf():
    response = headers.get(headers.json_info.get("Pockets"))
    # print(response)
    if response['status']['httpCode'] != 200:
        return "[Ⅹ]cookie information is invalidated!"
    for data in bookshelf['data']:
        for novels in data['expand']['novels']:
            authorName = novels['authorName']
            novelName = novels['novelName']
            novelId = novels['novelId']
            bookshelfs = "\n书名：{}\n作者：{}\n序号：{}".format(novelName, authorName, novelId)
            print(bookshelfs)


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


def shell():
    inputs = sys.argv[1:]
    if inputs[0] == "s" or inputs[0] == "search":
        search_json(*re_novel_id(inputs[1]))
    # elif inputs[0].startswith('fx'):
    #     direction.WebRecommendation().wind_show_info()
    # elif inputs[0].startswith('name'):
    #     shell_book_name(inputs)
    elif inputs[0] == "sf" or inputs[0] == "bookshelf":
        bookshelf()
    #     thumbs_up.Support().run_script() if mode else thumbs_up.Support()
    # elif inputs[0].startswith('up'):
    #     show_book_up_data(inputs)
    else:
        print(inputs[0], "不是有效命令")


if __name__ == '__main__':
    shell()
