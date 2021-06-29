import requests
from bs4 import BeautifulSoup as bs
import csv
import os
import datetime


host = 'https://www.x-kom.pl'
url = 'https://www.x-kom.pl/g-5/c/11-procesory.html'
page_part = '?page='
HEADERS = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_total_pages(html):
    soup = bs(html, 'lxml')
    total_pages = soup.find('div', class_='sc-1xy3kzh-7 kwXVqA').findAll('a')[-1].text
    return int(total_pages)


def write_csv(data):
    file_name1 = url.split('/')[-1].split('.')[0]
    file_name2 = ''
    for c in file_name1:
        if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'):
            file_name2 = file_name2 + c
            if file_name2 == 'procesory':
                file_name2 = 'Процессоры'
            elif file_name2 == 'dyskitwardehddissd':
                file_name2 = 'SSD диски'
            elif file_name2 == 'kartygraficzne':
                file_name2 = 'Видеокарты'

    with open(file_name2 + '.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((data['title'],
                         data['price'],
                         data['url']))
        print(data['title'], '/', data['price'], 'успешно спарсено!')


def get_page_data(html):
    soup = bs(html, 'lxml')
    ads = soup.find('div', id='listing-container').find_all('div', class_='sc-162ysh3-1')
    for ad in ads:
        try:
            title = ad.find('h3').text.strip()
        except:
            title = 'title error'
        try:
            price = ad.find('span', class_='sc-6n68ef-0').text.split(' z')[0]
        except:
            price = 'price error'
        try:
            url = host + ad.find('a').get('href')
        except:
            url = 'url error'
        data = {'title': title,
                'price': price,
                'url': url}
        write_csv(data)


def main():
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages + 1):
        print(f'Парсинг страницы {i} из {total_pages}...')
        url_gen = url + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == "__main__":
    main()
