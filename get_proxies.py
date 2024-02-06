import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures

#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

if __name__=='__main__':
    proxylist = getProxies()

    with open('./expo/proxies/scraped_proxies.txt', 'w') as file:
        # Write each element to the file followed by a newline character
        for p in proxylist:
            file.write("%s\n" % p)