from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import csv


URL = "https://new.land.naver.com/complexes?ms=35.163207,129.1637,15&a=APT:ABYG:JGC&e=RETAIL"
driver = webdriver.Chrome()


def save_to_land(land):
    f = open("부동산수정.csv", 'w', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow(['번호', '매물명', '매매', '전세', '월세', '면적'])

    for i in land:
        print(i)
        writer.writerow(list(i.values()))
    return


def extract_land():

    place = []
    th = ''
    driver.get(URL)
    num = 0
    time.sleep(3)

    html = driver.page_source
    soup = bs(html, 'html.parser')

    land = soup.select('.complex_infos')
    for i in land:
        title = i.find('div', {'class':  'complex_title'}).text
        price = i.find_all('div', {'class':  'complex_price'})
        area = i.find('dd', {'class': 'complex_size-default'}).text
        if(price != [] and area != '- ㎡'):

            Trading = "-"  # 매매

            charter = "-"  # 전세

            monthly = "-"  # 월세
            num += 1
            for pr in price:
                ty = pr.find('span', {'class': 'type'}).get_text()
                if(ty == "매매"):
                    Trading = pr.find(
                        'span', {'class': 'price_default'}).get_text()
                elif(ty == "전세"):
                    charter = pr.find(
                        'span', {'class': 'price_default'}).get_text()
                elif(ty == "월세"):
                    c = pr.find(
                        'span', {'class': 'price_default'}).get_text()
            place.append({'num': num, 'title': title,
                          'Trading': Trading, 'charter': charter, 'monthly': monthly, 'area': area})
    driver.close()
    driver.quit()
    return place


some = extract_land()

save_to_land(some)
