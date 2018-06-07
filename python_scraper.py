import re
import sqlite3
from urllib.request import urlopen
from html import unescape

def main():
    '''
    メインの処理。fetch(), scrape(). save() の3つの関数を呼び出す。
    '''
    #html = fetch('https://gihyo.jp/dp')
    html = read('dp.html')
    books = scrape(html)
    save('books.db', books)

def fetch(url):
    '''
    :param url: 与えられたURLのWebページを取得する。WebページのエンコーディングはContent-Typeヘッダーから取得する
    :return: type str HTML
    '''
    f = urlopen(url)
    encoding = f.info().get_content_charset(failobj='utf-8')
    html = f.read().decode(encoding)
    return html

def read(file_path):
    '''
    :param file_path:
    :return: type str HTML
    '''
    with open(file_path) as f:
        html = f.read()
    return html

def scrape(html):
    '''
    :param html: 与えられたHTMLから正規表現で書籍の情報を抜き出す。
    :return: 書籍(dict)のリスト
    '''
    books = []
    for partial_hrml in re.findall(r'<a itemprop="url".*?</ul>\s*</a></li>', html, re.DOTALL):
        url = re.search(r'<a itemprop="url" href="(.*?)">', partial_hrml).group(1)
        url = 'https://gihyo.jp' + url
        title = re.search(r'<p itemprop="name".*?</p>', partial_hrml).group(0)
        title = re.sub(r'<.*?>', '', title)
        title = unescape(title)
        books.append({'url': url, 'title': title})
    return books

def save(db_path, books):
    '''
    :param db_path: SQLiteのDB Path
    :param books: 与えられた書籍のリストをSQLiteデータベースへ保存する。
    :return: null
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS books')
    c.execute('''
        CREATE TABLE books (
            title text,
            url text
        )
    ''')
    c.executemany('INSERT INTO books VALUES (:title, :url)', books)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()