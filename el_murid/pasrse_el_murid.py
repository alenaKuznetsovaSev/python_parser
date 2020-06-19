from bs4 import BeautifulSoup
import requests
import lxml
import re

import pandas as pd

url = '/home/al/Downloads/al-murid.html'
bs = BeautifulSoup(open(url), 'lxml')

person = {}

#'Nick': '',
#'url_blog': '',
#'Comments': [],

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
for comment in all_comments:
    comm = comment.parent.parent
    #first_comment_block = all_comments[0].parent.parent # получение одного блока коментария (текст и автор)
    #print(first_comment_block)
    author_block = comm.find('a', class_='i-ljuser-username')
    #author_block = first_comment_block.find('a', class_='i-ljuser-username')
    author_nick = str(author_block.b.text)
    comment_text = comm.td.next_sibling.text
    comment_text = re.sub('Edited.*', '', comment_text)  # удаляем Edited и всё после него
    print('Автор комментария: ' + author_nick)
    if author_nick not in person: #новый автор
        person[author_nick] = {'url_blog': '', 'Comments': [], }
        author_link = author_block['href']  # ссылка на его журнал
        person[author_nick]['url_blog'] = author_link
        print('Ссылка на страницу автора: ' + str(author_link))
        person[author_nick]['Comments'].append(comment_text)
    else:
        person[author_nick]['Comments'].append(comment_text)
    print('Текст комментария: ' + comment_text)

#добавляем в структуру

print(person)