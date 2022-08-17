import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {'User-Agent':  # маска под которой будут отправляться запросы на сервер
           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5 Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)'}

def download(url):
    resp = requests.get(url, stream=True)
    r = open('/Users/unknown1/Documents/Python/Parsing/image/' + url.split('/')[-1], 'wb')
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()



def get_url():

    for count in range(1, 8):  # цикл для прохождения страниц вебсайта (в этом случае 8 страниц различных вещей)

        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'  # страница сайта для парсинга

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        data = soup.find_all('div', class_="col-lg-4 col-md-6 mb-4")  # собирает данные с контейнера с одеждой

        for i in data:  # цикл для помещение всех слотов одежды на странице сайта в генератор
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url  # генератор для оптимизации кода и меньшего потребления памяти


def array():

    for card_url in get_url():

        response = requests.get(card_url, headers=headers)

        sleep(1)  # перерыв между запросами на сайт, для ограничения, чтобы не обвалить процессы (3 секунды оптимальное значение)

        soup = BeautifulSoup(response.text, 'lxml')  # парсинг

        data = soup.find('div', class_="card mt-4 my-4")  # собирает данные о целом слоте одежды

        name = data.find('h3', class_="card-title").text  # название одежды
        url_img = 'https://scrapingclub.com' + data.find('img', class_="card-img-top img-fluid").get('src')  # ссылка на картинку слота одеждой
        price = data.find("h4").text  # цена слота одежды
        text = data.find('p', class_="card-text").text  # описание слота одежды

        download(url_img)

        yield name, url_img, price, text
