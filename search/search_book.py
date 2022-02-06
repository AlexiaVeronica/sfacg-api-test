import argparse
import re
import sys
import json


def tag_(tag):
    return ', '.join([tags['tagName'] for tags in tag])


def re_novel_id(book_id: str):
    book_id = book_id if 'http' not in book_id else \
        re.findall(r'/([0-9]+)/?', book_id)[0]
    if book_id.isdigit():
        return book_id, 200
    else:
        return f'输入信息 {book_id} 不是数字！', 403


def search_json(novel_id, code):
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
    parser.add_argument("book_name", help="please input the [novel name]")
    args = parser.parse_args()
    book_id = args.book_id
    book_name = args.book_name
    convert = args.f
    try:
        search_json(*re_novel_id(book_id))
    except KeyError:
        print('搜索信息不存在')


if __name__ == '__main__':
    main()
