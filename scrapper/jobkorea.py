import requests
from bs4 import BeautifulSoup
from sqlite33 import jobskorea_insert


def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    # print(soup)
    pagination = soup.find('div', {'class': 'tplPagination newVer wide'})
    links = pagination.find_all('li')

    pages = []
    for link in links:
        pages.append(int(link.text))

    max_pages = pages[-1]
    return max_pages


def extract_job(html):
    title = html.find('a', {'class': 'name dev_view'}).get_text()
    if title != '파이썬' and title != '피톤힐링':
        location = html.find('span', {'class': 'loc long'}).get_text()
        content = html.find('a', {'class': 'title dev_view'})["title"]
        return {'title': title, 'location': location, 'content': content}


def extract_jobs(last_pages, URL):
    jobs = []
    num = 0
    for page in range(last_pages):
        print(f"Scrapping page {page+1} ")
        result = requests.get(f"{URL}&Page_No={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        # 첫번째 lists만 출력함 전부다 찾으면 이상하게 나옴
        article = soup.find('div', {'class': 'lists'})
        results = article.find_all('div', {'class': 'post'})
        for result in results:
            num += 1
            company = result.find('a', {'class': 'name dev_view'}).get_text()
            spec = result.find('span', {'class': 'exp'}).get_text()
            location = result.find(
                'span', {'class': 'loc long'}).get_text()
            content = result.find(
                'a', {'class': 'title dev_view'})["title"]
            link = result.find('a', {'class': 'title dev_view'})['href']
            jobskorea_insert(num, company, spec, content, link)
            jobs.append(
                {'num': num, 'company': company, 'spec': spec, 'location': location, 'content': content, 'link': f"https://www.jobkorea.co.kr{link}"})
        # print(jobs)

    return jobs


def get_jobs(word):
    URL = f'https://www.jobkorea.co.kr/Search/?stext={word}'
    last_pages = get_last_page(URL)
    jobs = extract_jobs(last_pages, URL)
    return jobs
