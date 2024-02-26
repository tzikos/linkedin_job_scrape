import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import random
from concurrent.futures import ThreadPoolExecutor
import hashlib

timestamp = str(datetime.now())
timestamp = str(timestamp).split(':')[0]+':'+str(timestamp).split(':')[1]
keywords = os.environ["KEYWORDS"]
location = os.environ["LOCATION"]


with open('./expo/proxies/working_proxies.txt','r') as f:
    proxylist = f.read().split('\n')
proxylist = [p for p in proxylist if len(p)>0]

with open(f'./expo/txt/{timestamp}_job_ids.txt', "r") as file:
    job_ids = [int(line.strip()) for line in file]


def generate_hash_key(data):
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def get_job_data(job_id,proxylist=proxylist):
    job_posting_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    job_info = {}
    if len(proxylist)==0:
        print('No proxies available.')
    else :
        try:
            proxy = random.choice(proxylist)
            print(f'Using proxy: {proxy}')
            resp = requests.get(job_posting_url.format(job_id),
                            proxies={'http' : proxy,'https': proxy}, 
                            timeout=2)
            soup = BeautifulSoup(resp.text, 'html.parser')

            job_info["scrape_date"] = str(timestamp)

            try:
                job_info["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
            except:
                job_info["company"] = None

            try:
                job_info["location"] = soup.find("div", {"class": "topcard__flavor-row"}).find("span", {'class': 'topcard__flavor--bullet'}).text.strip()
            except:
                job_info["location"] = None

            try:
                job_info['posted_time_ago'] = soup.find_all("div", {"class": "topcard__flavor-row"})[1].find('span', {'class': 'posted-time-ago__text'}).text.strip()
            except:
                job_info['posted_time_ago'] = None

            try:
                job_info['applicant_number'] = soup.find_all("div", {"class": "topcard__flavor-row"})[1].find('span', {'class': 'num-applicants__caption'}).text.strip()
            except:
                job_info['applicant_number'] = None

            try:
                job_info["job_title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
            except:
                job_info["job_title"] = None

            try:
                job_info["job_description"] = soup.find("div", {"class": "description__text description__text--rich"}).text.strip()
            except:
                job_info["job_description"] = None

            try:
                job_info["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace("Seniority level", "").strip()
            except:
                job_info["level"] = None

            try:
                job_info["employment_type"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all("li")[1].text.replace("Employment type", "").strip()
            except:
                job_info["employment_type"] = None

            try:
                job_info["job_function"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all("li")[2].text.replace("Job function", "").strip()
            except:
                job_info["job_function"] = None

            try:
                job_info["industries"] = soup.find("ul", {"class": "description__job-criteria-list"}).find_all("li")[3].text.replace("Industries", "").strip()
            except:
                job_info["industries"] = None
                
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving job data for job ID {job_id}: {e}")

    return job_info

if __name__ == "__main__":
    print('Reading proxies.....')
    print('Getting Job data.......')
    
    jobs_data = []
    with ThreadPoolExecutor() as executor:
        for row in executor.map(get_job_data, job_ids):
            jobs_data.append(row)

    df = pd.DataFrame(jobs_data)
    if len(df)>0:
        # df['for_hash']=df.apply(lambda row : row["company"]+row['location']+row['job_title']+row['level']+row['employment_type']+row['job_function']+row['industries'],axis=1)
        # df['hash'] = df['for_hash'].apply(lambda x : generate_hash_key(x))
        # df.drop(columns=['for_hash'],inplace=True)
        df.to_csv(f'./expo/csv/{keywords}_{location}_{timestamp.split(".")[0]}_linkedinjobs.csv', index=False, encoding='utf-8')
        print(f"Number of jobs scraped: {len(df)}")
    else:
        'Empty dataframe'
