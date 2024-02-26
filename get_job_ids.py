import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import os
from datetime import datetime
import random

keywords = os.environ["KEYWORDS"]
location = os.environ["LOCATION"]

def get_job_ids(keywords, location):
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
    start = 0
    target_url = base_url + f'keywords={quote(keywords)}&location={quote(location)}&f_TPR=r604800'
    job_ids = []

    print('Reading proxies.....')
    with open('./expo/proxies/working_proxies.txt','r') as f:
        proxylist = f.read().split('\n')
        
    proxylist = [p for p in proxylist if len(p)>0]

    if len(proxylist)==0:
        print('No proxies available.')
    else :
        print(f'Found {len(proxylist)} proxies!\n')
        print('\nScraping Job IDs.....')
        while start != -1:

            proxy = random.choice(proxylist)
            print(f'Using proxy: {proxy}')

            try : 
            
                res = requests.get(target_url + f'&start={start}',
                                   proxies={'http' : proxy,'https': proxy}, 
                                   timeout=2)
                
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
            except :
                print(f'Problem with proxy {proxy} in {target_url}&start={start}')

    return job_ids

if __name__ == "__main__":
    job_ids = get_job_ids(keywords, location)
    print('Job IDs scraped: ',len(job_ids))
    timestamp = str(datetime.now())
    timestamp = str(timestamp).split(':')[0]+':'+str(timestamp).split(':')[1]
    with open(f"./expo/txt/{timestamp}_job_ids.txt", "w") as file:
        for job_id in job_ids:
            file.write(str(job_id) + "\n")
