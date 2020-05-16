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
#print('Ссылка на первую статью блога автора: ' + first_article_link)     # берет юрл верхней (последней) статьи

#<a class="comments-pages-button" href="https://mylnikovdm.livejournal.com/352147.html?page=2#comments" target="_self"><span class="arrow arrow--right">→</span></a>
url_into = '/home/al/Downloads/longCommliveJournal2.html'

def parsing_one_page(url: str) -> set:
    """разбирает одну страницу"""
    bs_into = BeautifulSoup(open(url), 'lxml')
    #детекция next_button
    next_button = bs_into.find_all('span', class_='comments-pages-button-disabled')
    #if next_button[1].find(class_='arrow--right'):
        #print('Достгнута последняя страница комментариев')
    #print(next_button[1].find(class_='arrow--right'))
    all_comments = bs_into.find_all('div', class_='comment-text')
    # print(all_comments)
    for comment in all_comments:
        # print(comment.text)
        block_nick = comment.find_previous_sibling().find('a', class_='i-ljuser-username')
        author_nick = block_nick.text
        # print(author_nick)
        comment = re.sub('Edited.*', '', comment.text)  # удаляем Edited и всё после него
        # print('Автор комментария: ' + author_nick)
        if author_nick not in person:  # новый автор
            person[author_nick] = {'url_blog': '', 'Comments': [], }
            author_link = block_nick['href']  # ссылка на его журнал
            person[author_nick]['url_blog'] = author_link
            # print('Ссылка на страницу автора: ' + str(author_link))
            person[author_nick]['Comments'].append(comment)
        else:
            person[author_nick]['Comments'].append(comment)
        # print('Текст комментария: ' + comment)
    return person

parsing_one_page(url_into)

print(person)