import requests 
import hashlib
from urllib.parse import urlparse
from pprint import pprint
from bs4 import BeautifulSoup as bs

### Utils ###

def hashFromString(someString): 
    return hashlib.md5(someString.encode()).hexdigest()

def getSiteName(site):
    return urlparse(site).netloc

def getSiteContent(url): 
    return requests.get(url).text
### /Utils ###


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
    return [{
        'link': a.get('href'), 
        'rel': a.get('rel'), 
        'title': a.get('title'),
        'hash': a.get('href'),
    } for a in links if a.get('href') and sitename in a.get('href')]

# add to the list
def analyzeContent(sites, tags):
    results = {}
    for site in sites: 
        siteContent = getSiteContent(site)
        siteName = getSiteName(site)
        siteHash = hashFromString(site)
        content = {
            'name' : siteName,
            'links': getSiteNavigation(siteContent, siteName),
            'hash' : hashFromString(site) 
        }
        results[siteHash] = content
    
    return results


def extractTagsFromPage(content, tags):
    retrived = {}
    scrapper = bs(content, 'lxml')
    for tag in tags: 
        target = scrapper.find_all(tag.strip())  # strip tag in case it contains spaces
        retrived[tag] = len(target)

    return retrived

def getPageMockContent(): 
    with open('./tests/primaria.html') as f:
        content = f.read()
        if (content):
            return content;
def main(): 
    ''' get sites and tags from the lists'''
    tags = getListOfTags()
    sites = getListOfSites()
    ''' create a dictionary '''
    results = analyzeContent(sites, tags)
    ''' TODO analize content and extract the tags from content '''
    for result in results:
        target = results[result]
        if (len(target['links']) == 0): 
            print(target['name'] + ' has no links to parse')
            break
        links = target['links'][:10];
        for idx,adr in enumerate(links):
            content = getSiteContent(adr['link'])
            tagsInContent = extractTagsFromPage(content, tags)
            links = getSiteNavigation(content, target['name'])
            newLinks = [l for l in links if len([el for el in target['links'] if el['hash'] == l['hash']]) == 0]
            print(idx, target['name'], adr['link'], tagsInContent, len(newLinks), ' new links')

        

    # tagsInContent = extractTagsFromPage(getPageMockContent(), tags)
    # findMoreLinks = getSiteNavigation(getPageMockContent())
    ''' TODO create table with results'''


if __name__=='__main__':
    main()