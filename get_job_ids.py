import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import os
from datetime import datetime

keywords = os.environ["KEYWORDS"]
location = os.environ["LOCATION"]

def get_job_ids(keywords, location):
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
    start = 0
    target_url = base_url + f'keywords={quote(keywords)}&location={quote(location)}'
    job_ids = []

    while start != -1:
        res = requests.get(target_url + f'&start={start}')
        if len(re.sub('[\n <!->]', '', res.text)) > 0:
            soup = BeautifulSoup(res.text, 'html.parser')
            all_jobs_on_this_page = soup.find_all("li")

            for x in range(0, len(all_jobs_on_this_page)):
                try:
                    job_id = all_jobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                    job_ids.append(job_id)
                except:
                    pass

            print(f'{len(job_ids)}',end='\r')           
            start += 25
        else:
            start = -1

    return job_ids

if __name__ == "__main__":
    print('Scraping Job IDs.....')

    job_ids = get_job_ids(keywords, location)
    print('Job IDs scraped: ',len(job_ids))
    timestamp = str(datetime.now())
    timestamp = str(timestamp).split(':')[0]+':'+str(timestamp).split(':')[1]
    with open(f"./expo/{timestamp}_job_ids.txt", "w") as file:
        for job_id in job_ids:
            file.write(str(job_id) + "\n")
