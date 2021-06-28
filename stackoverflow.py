import requests
from bs4 import BeautifulSoup
URL = 'https://stackoverflow.com/jobs?q=python'


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    s = []
    for link in pages[:-1]:
        s.append(link.find('span'))
    else:
        last_page = s[(-1)].get_text(strip=True)
        return int(last_page)


def extract_job(html):
    title = html.find('a')['title']
    company, location = html.find('h3').find_all('span')
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html.find('a', {'class': 's-link'})['href']
    return {'title': title,
            'company': company,  'location': location,  'link': f"https://stackoverflow.com{job_id}"}


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'grid--cell fl1'})
        for result in results:
            jobs.append(extract_job(result))
        else:
            return jobs


def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs
