import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.text))
    else:
        max_pages = pages[(-1)]
        return max_pages


def extract_job(html):
    title = html.find('div', {'class': 'heading4'}).text
    company = html.find('span', {'class': 'companyName'}).text
    location = html.find('div', {'class': 'companyLocation'}).text
    job_id = html['data-jk']
    return {'title': title,  'company': company,  'location': location,  'link': f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('a', {'class': 'tapItem'})
        for result in results:
            jobs.append(extract_job(result))
        else:
            return jobs


def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs
