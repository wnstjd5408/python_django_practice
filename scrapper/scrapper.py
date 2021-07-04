import requests
from bs4 import BeautifulSoup


def get_last_page(URL):
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
    company, location = html.find('h3').find_all('span', recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html.find('a', {'class': 's-link'})['href']
    return {'title': title,
            'company': company,  'location': location,  'link': f"https://stackoverflow.com{job_id}"}


def extract_jobs(last_pages, URL):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'grid--cell fl1'})
        # print(results)
        for result in results:
            jobs.append(extract_job(result))

    return jobs


def get_jobs(word):
    URL = f'https://stackoverflow.com/jobs?q={word}'
    last_pages = get_last_page(URL)
    jobs = extract_jobs(last_pages, URL)
    return jobs
