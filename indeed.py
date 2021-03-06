import requests
from bs4 import BeautifulSoup
import urllib3

# disable any Python warnings: InsecureRequestWarning: Unverified HTTPS request is being made
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&l=United+States&limit={LIMIT}'

def get_last_page():
    # 'certificate verify failed' 발생시 verify=False 추가
    resul = requests.get(URL, verify=False)
    soup = BeautifulSoup(resul.text, 'html.parser')
    pagination = soup.find('div', {'class':'pagination'})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find('div', {'class':'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    if company is not None:
        company_anchor = company.find('a ')
        if company_anchor is not None:
            company = str(company_anchor.string).strip()
        else:
            company = str(company.string).strip()
    else:
        company = "No company info"
    location = html.find('div', {'class':'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://www.indeed.com/viewjob?jk={job_id}'
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page {page}")
        resul = requests.get(f"{URL}&start={page*LIMIT}", verify=False)
        soup = BeautifulSoup(resul.text, 'html.parser')
        results = soup.find_all('div', {'class':'jobsearch-SerpJobCard'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs
