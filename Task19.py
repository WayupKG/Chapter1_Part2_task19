import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Возвращает HTML код страницы
def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    div_links = soup.find('div', class_='category-items-outer').find_all('article', class_='listing-item')

    links = []

    for div in div_links:
        a = div.find('a').get('href')
        link = "https://lalafo.kg" + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = soup.find('h2', class_= 'adv-title').text.strip()
    except:
        name = ""
    try: 
        sena = soup.find('span', class_= 'price').text.strip()
    except:
        sena = ""
    data = {'name': name,
            'sena': sena}
    return data
    
def write_csv(data):
    with open('telefon-web.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow((data['name'],
                         data['sena']))
        print(data['name'], 'parsed')

def main():
    start = datetime.now()

    url = "https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony/xiaomi?currency=KGS"
    all_links = get_all_links( get_html(url) )

    for url in all_links:
        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)

    end = datetime.now()

    totol = end - start
    print(str(totol))



if __name__ == '__main__':
    main()