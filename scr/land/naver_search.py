from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
import sys
import re

URL = "https://m.place.naver.com/restaurant/list?x=129.1023126&y=35.1385167&query="
plus = input("장소를 입력하시오 : ")

URL = URL + plus

subway_location = ""
opentime = []
place = []
imageurl = []
num = 0
stop = 0
count = 0
driver = webdriver.Chrome(
    executable_path="D:/파이썬 공부/web/Python-update/scr/land/chromedriver.exe")
driver.implicitly_wait(20)
driver.get(URL)

URL = driver.current_url

# 크롤링 한 화면을 클릭해서 크롤링하는거


def click_nolink_for_scrollDown(driver):
    while True:
        try:
            plus = driver.find_element_by_css_selector(
                "#app-root > div > div > div.place_detail_wrapper > div.place_fixed_maintab > div > div > div > div > a:nth-child(1)")
            plus.click()
            break
        except:
            driver.refresh()
            time.sleep(1)

    time.sleep(0.1)
    for i in range(10):
        time.sleep(0.2)
        driver.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)

# 파일을 csv 파일에 저장


def save_to_place(name, place):
    f = open(name, 'w+', newline='',  encoding='utf-8-sig')
    writer = csv.writer(f)
    for i in place:
        writer.writerow(list(i.values()))
    return

# 이름명이 동일한 csv 파일명을 바꾸어주는 메서드


def check(file_name):
    file_ext = '.csv'
    output_path = 'D:/파이썬 공부/web/Python-update/scr/land/new/%s%s' % (
        file_name, file_ext)
    uniq = 1
    while os.path.exists(output_path):
        output_path = 'D:/파이썬 공부/web/Python-update/scr/land/new/%s(%d)%s' % (
            file_name, uniq, file_ext)
        uniq += 1
    return output_path


ht = driver.page_source
so = bs(ht, 'html.parser')
# body라는 것을 find_element_by_css_selector로 찾고나서 ul을 한 번 눌려준다
try:
    body = driver.find_element_by_css_selector("body")
    time.sleep(0.3)
    driver.find_element_by_css_selector(
        '#_list_scroll_container > div > div > div:nth-child(2) > ul').click()
#
    for i in range(500):  # 첫페이지의 길이만큼이나 안에 있는 숫자를 늘려주고 줄여줄 수 있다.
        time.sleep(0.2)
        body.send_keys(Keys.PAGE_DOWN)
except:
    driver.refresh()
    time.sleep(1)

plus = check(plus)
while True:
    opentime.clear()
    num += 1
    score = ""
    blog = ""
    visit = ""
    imageurl = ""
    try:
        # 첫페이지때 이미지를 imageurl라는 변수에 저장
        image = driver.find_element_by_xpath(
            f'//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[{num}]/div[2]/div/a[1]/span/div')
        # //*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[1]/div[2]/div/a[1]/span/div
        im = image.get_attribute('style')
        found = im.find('(')
        imageurl = im[found+2::][:-3]

        # find_element_by_xpath로 위치를 찾아서 클릭을 해준다
        driver.find_element_by_xpath(
            f'//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[{num}]/div[1]/a[1]').send_keys(Keys.CONTROL + "\n")
        # driver.find_element_by_css_selector(
        #     f"#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({num}) > div.Ow5Yt > a:nth-child(1)").send_keys(Keys.CONTROL + "\n")
        stop = 0
        count += 1
    except:
        # 찾지를 못하면 stop의 숫자를 늘려주고 5가 되면 break문을 걸어서 종료
        driver.execute_script('window.scrollTo(0, 400);')
        stop += 1
        print(stop)
        if(stop == 5):
            break
        continue

    # 열어준 탭이동을 합니다

    driver.switch_to_window(driver.window_handles[-1])

    time.sleep(1)

    click_nolink_for_scrollDown(driver)
    # 페이지를 클릭하여서 새로운 정보를 크롤링을 한다
    time.sleep(0.1)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    name = soup.find('span', {'class': '_3XamX'}).text
    info = soup.find('span', {'class':  '_3ocDE'}).text
    avg = soup.find('div', {'class': '_1kUrA'})
    score_visit_blog = avg.find_all('span',  {'class': '_1Y6hi'})

    if len(score_visit_blog) == 1:
        if '방문자리뷰' in score_visit_blog[0].find('a').text:
            visit = score_visit_blog[0].find('em').text
        elif '블로그리뷰' in score_visit_blog[0].find('a').text:
            blog = score_visit_blog[0].find('em').text
    elif len(score_visit_blog) == 2:
        try:
            if score_visit_blog[0].find('span', {'class': 'place_blind'}).text == '별점':
                if "블로그리뷰" in score_visit_blog[1].find('a').text:
                    score = score_visit_blog[0].find('em').text
                    blog = score_visit_blog[1].find('em').text
                else:
                    score = score_visit_blog[0].find('em').text
                    visit = score_visit_blog[1].find('em').text
        except:
            visit = score_visit_blog[0].find('em').text
            blog = score_visit_blog[1].find('em').text

    elif len(score_visit_blog) == 3:
        score = score_visit_blog[0].find('em').text
        visit = score_visit_blog[1].find('em').text
        blog = score_visit_blog[2].find('em').text
    # print(f'별점 : {score}, 방문자리뷰  :  {visit} , 블로그 리뷰 : {blog}')
    data = soup.find_all('div', {'class': '_1h3B_'})

    location = data[0].find('span', {'class': '_2yqUQ'}).text
    try:
        subway_location = data[0].find('div', {'class': '_2P6sT'})
        subway_number = subway_location.find('span', {'class': '_12Coj'}).text
        subway_location = subway_location.text
    except:
        subway_location = None
    print(subway_location)
    t = data[1].find_all('div', {'class': '_2ZP3j'})
    if(len(t) == 1):
        tt = t[0].text
    else:
        for i in t:
            try:
                etc = i.find('div', {'class': '_20pEw'}).text
            except:
                etc = i.find('span', {'class': '_20pEw'}).text

            opentime.append(etc)

        tt = ",".join(opentime)
        # place를 리스트에 딕셔너리 형태로 저장을 시킨다
    place.append({"num": num,  "name": name, "info": info, "score": score, "visit": visit, "blog": blog,
                  "location": location, "subway_location": subway_location, "clock":  tt, "imageurl": imageurl})
    print(f'{count} : {name}')
    save_to_place(plus, place)
    # driver를 종료하고 전에있던 탭을 켜줍니다.
    driver.close()

    driver.switch_to_window(driver.window_handles[0])


driver.quit()
