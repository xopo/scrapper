import requests 
import hashlib
from urllib.parse import urlparse
from os.path import join

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

import re
import time
from fileHelpers import readContentFromFile, writeCachedContent

driver = None

def getDriver():
    return webdriver.PhantomJS()

### Utils ###
def hashFromString(someString): 
    return hashlib.md5(someString.encode()).hexdigest()

def getSiteName(site):
    return urlparse(site).netloc

def phantomGetContent(url):
    if not driver:
        driver = getDriver()

    driver.get(url)
    time.sleep(5)
    return driver.page_source

# get page content, use driver for dinamic content
def getLiveSiteContent(url): 
    try:
        html = requests.get(url).text
        if len(html) < 1000:
            return phantomGetContent(url)
        return html
    except:
        print(er)
        try:
            return phantomGetContent(url)
        except:
            time.sleep(10)
            print('error getting data for - %s' % url)
            return ''
    
'''check for cached version
- try request first 
- use phantomJs for js sites
'''
def getSiteContent(url):
    siteHash = hashFromString(url)
    # check contentFileExists
    cachedContent = join('cache', siteHash)

    content = readContentFromFile(cachedContent, False)
    if content and len(content) > 5000:
        return content
    content = getLiveSiteContent(url)
    if content and len(content):
        writeCachedContent(cachedContent, content)
        return content
    

'''
    get list of links
    use sitename to distinguish between internal and external links
    return [internal, external]
'''
def getSiteNavigation(content, sitename):
    scrapper = bs(content, 'lxml')
    links = scrapper.find_all('a')
    internalLinks = [{
        'link': a.get('href'), 
        'rel': a.get('rel'), 
        'title': a.get('title'),
        'hash': hashFromString(a.get('href')),
    } for a in links if a.get('href') and sitename in a.get('href')]
    externalLinks = [a.get('href') for a  in links if a.get('href') and 'http' in a.get('href') and not sitename in a.get('href')]
    return [internalLinks, externalLinks]

'''clean word by removing extra punctuation and change to lowercase'''
def prepareSearch(word): 
    regex = re.compile('[^a-z\-]')
    return regex.sub('', word.lower())

'''for each elements check site analitics'''
def findMetaInTags(elements, analitics):
    dups = []
    result = {'all': 0}
    if len(elements) == 0 or not analitics: return 0
    for element in elements:
        content = element.text
        if len(content) == 0: continue
        content = content.lower().strip().split(' ')
        for key in analitics:
            print('--key', key)
            if not key in result:
                result[key] = {"all": 0}
            targets = analitics[key]
            if not targets: continue
            for target in targets.split(' '):
                target = prepareSearch(target)
                if target in dups: continue
                dups.append(target)
                if len(target) < 5: continue 
                targetFound = content.count(target)
                if targetFound > 0:
                    result['all'] = result['all'] + targetFound
                    result[key]['all'] = result[key]['all'] + targetFound
                    result[key][target] = targetFound
                print(target, result)
    print(result)
    return result

def extractTagsFromPage(content, tags, analitics):
    retrived = {}
    scrapper = bs(content, 'lxml')
    for tag in tags: 
        target = scrapper.find_all(tag.strip())  # strip tag in case it contains spaces
        retrived[tag] = {
            'count': len(target),
            'metaScore': findMetaInTags(target, analitics)
        }

    return retrived

def getMetaData(meta, content):
    retreived = []
    scrapper = bs(content, 'lxml')
    if meta == 'title':
        return scrapper.find(meta).text
    targets = scrapper.find_all('meta')
    for target in targets:
        if target.has_attr('name') and target['name'] == meta:
            print(meta, target['content'])
            return target['content'] if target.has_attr('content') else '' 
    