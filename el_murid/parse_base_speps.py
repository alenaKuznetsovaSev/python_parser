from bs4 import BeautifulSoup
import requests
import lxml

import pandas as pd

url = '/home/al/Downloads/al-murid.html'
bs = BeautifulSoup(open(url), 'lxml')

"""
search_url = f'http://www.best-cd-price.co.uk/search-Keywords/1-/229816/sex+pistols.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
page = requests.get(search_url, headers=headers)
if page.status_code == requests.codes.ok:
  print('Everything is cool!')
"""
list_all_headers = bs.find_all('a', class_='subj-link')
first_article_link = list_all_headers[0]['href']
print('Ссылка на первую статью блога автора: ' + first_article_link)     # берет юрл верхней (последней) статьи


url_into = '/home/al/Downloads/al-murid-into.html'
bs_into = BeautifulSoup(open(url_into), 'lxml')
all_comments = bs_into.find_all('div', class_='commentText')
first_comment_block = all_comments[0].parent.parent # получение одного блока коментария (текст и автор)
#print(first_comment_block)

author_block = first_comment_block.find('a', class_='i-ljuser-username')
#print(author_block)
comment_author = author_block.b.text #ник автора комента
print('Автор комментария: ' + str(comment_author))
author_link = author_block['href'] #ссылка на его журнал
print('Ссылка на страницу автора: ' + str(author_link))
comment_text = first_comment_block.td.next_sibling.text
print('Текст комментария: ' + comment_text)
