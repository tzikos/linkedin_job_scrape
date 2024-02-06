import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures

def check(proxy):
    #this was for when we took a list into the function, without conc futures.
    #proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2).status_code
    except :
        r = 'failed'
    return proxy, r

with open('./expo/proxies/scraped_proxies.txt','r') as f:
    proxylist = f.read().split('\n')

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(check, proxy) for proxy in proxylist]

working_proxies = [result.result()[0] for result in results if result.result()[1]==200]

with open('./expo/proxies/working_proxies.txt','w') as f:
    for wp in working_proxies:
        f.write("%s\n" % wp)



