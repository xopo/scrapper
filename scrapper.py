import requests 
import hashlib
from urllib.parse import urlparse
from pprint import pprint
from bs4 import BeautifulSoup as bs

def getListOfTags(): 
    with open('./tags') as f:
        content = f.read()
        if (content):
            tags = content.split('\n') 
            return [l.strip() for l in tags] if len(tags) else []
        

def getListOfSites(): 
    with open('./sites') as f:
        content = f.read()
        if (content):
            sites = content.split('\n') 
            return [s.split('-')[0].strip() for s in sites] if len(sites) else []

# get list of links
def getSiteNavigation(content, sitename):
    scrapper = bs(content, 'lxml')
    links = scrapper.find_all('a')
    return [{'link': a.get('href'), 'rel': a.get('rel'), 'title': a.get('title')} for a in links if a.get('href') and sitename in a.get('href')]

# add to the list

def analyzeContent(sites, tags):
    results = {}
    for site in sites[1:2]: 
        siteContent = requests.get(site)
        siteName = urlparse(site).netloc
        siteHash = hashlib.md5(site.encode()).hexdigest()
        content = {
            'name': siteName,
            'links': getSiteNavigation(siteContent.text, siteName)
        }
        results[siteHash] = content;
    
    pprint(results)
    return results

def main(): 
    tags = getListOfTags()
    sites = getListOfSites()
    results = analyzeContent(sites, tags);


if __name__=='__main__':
    main()