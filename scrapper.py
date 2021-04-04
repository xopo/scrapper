#!/usr/bin/env python3
from pprint import pprint
import json


from fileHelpers import isfile, join, getListOfTags, getListOfSites, readContentFromFile, writeCachedContent
from printerHelper import printSitesTable, printAllTagsTable
from htmlParser import hashFromString, getMetaData, getSiteName, getSiteContent, getSiteNavigation, extractTagsFromPage

# use a salt to cache result. if update is changed data will be gathered anew
update = 2

# add to the list
def analyzeContent(sites, tags):
    results = {}
    for site in sites['all']: 
        siteContent = getSiteContent(site)
        if not siteContent or len(siteContent) < 1000:
            continue 
        siteName = getSiteName(site)
        siteHash = hashFromString(site)
        content = {
            'name' : siteName,
            'links': getSiteNavigation(siteContent, siteName)[0],
            'hash' : hashFromString(site) ,
            'data' : {}
        }
        for meta in tags['# meta']:
            content[meta] = getMetaData(meta, siteContent)
        
        results[siteHash] = content
    
    return results

def uniqueLinks(links):
    unique = []
    dups = []
    for link in links:
        if not link['link'] in dups:
            unique.append(link)
            dups.append(link['link'])
    return unique;


def main(): 
    ''' get sites and tags from the lists'''
    tags = getListOfTags()
    sites = getListOfSites()
    searchEntity = hashFromString(json.dumps([ tags,  sites,  update]))
    resultFile = join('./results', searchEntity)
    print(resultFile)
    if isfile(resultFile):
        jsonResult = readContentFromFile(resultFile, False)
        results = json.loads(jsonResult)
    else: 
        results = analyzeContent(sites, tags)
        ''' TODO analize content and extract the tags from content '''
        for result in results:
            target = results[result]
            analitics = {
                'title': target['title'],
                'description': target['description'],
                'keywords': target['keywords']
            }
            if (len(target['links']) == 0): 
                print(target['name'] + ' has no links to parse')
                break
            links = uniqueLinks(target['links']) # [:10] # take first 10
            counter = -1 # so we start from 0
            while counter < 20:
                counter = counter + 1;        #for idx,adr in enumerate(links):
                print('\n\t\t%s %s' % (counter, target['name']))
                if len(links) <= counter:
                    counter = 51
                    break
                adr = links[counter]
                content = getSiteContent(adr['link'])
                if not content or len(content) == 0: 
                    continue
                try:
                    tagsInContent = extractTagsFromPage(content, tags['# html'], analitics)
                    [internalLinks, externalLinks] = getSiteNavigation(content, target['name'])
                    newLinks = [l for l in internalLinks if len([el for el in target['links'] if el['hash'] == l['hash']]) == 0]
                    if len(newLinks):
                        links = links + newLinks
                    print(counter, target['name'], adr['link'], tagsInContent, len(newLinks), ' new links')
                    results[result]['data'][adr['hash']] = {
                        'link': adr['link'],
                        'tags': tagsInContent,
                        'externalLinks': externalLinks
                    }
                except Exception as er: 
                    print('\n\n\terror:', er)
                    continue
        # save it for later change in parse data
        writeCachedContent(resultFile, json.dumps(results))

    parseResult(results)

def countTags(data): 
    tags = {}
    for key in data: 
        for tag in data[key]['tags']:
            if not tag in tags:
                tags[tag] = {
                    'count': 0,
                    'meta': 0
                }
            try:
                qty = data[key]['tags'][tag]['count']
            except:
                print('some error getting qty', data[key]['tags'][tag])
                qty = 0 
            try:
                metaScore = data[key]['tags'][tag]['metaScore']
                meta = metaScore['all'] if 'all' in metaScore else metaScore
            except:
                print('some error getting meta', data[key]['tags'][tag])
                meta = 0
            tags[tag]['count'] = tags[tag]['count'] + qty if tag in tags else qty
            tags[tag]['meta'] = tags[tag]['meta'] + meta if tag in tags else meta
            
    return tags;


def extractExternalLinks(data):
    extLinks = []
    for entry in data:
        page = data[entry]
        newLinks = [link for link in set(page['externalLinks']) if not link in extLinks]
        extLinks = extLinks + newLinks
    return extLinks

def parseResult(data):
    allTags = {}
    pretyObject = []
    parsedLinks = []
    for key in data: 
        entity = data[key]
        tags = countTags(entity['data'])
        externalLinks = extractExternalLinks(entity['data'])

        parsed = {
            'name': entity['name'],
            'links': len(entity['links']),
            'externalLinks': externalLinks,
            'tags' : tags,
        }
        parsedLinks.append(parsed)
        for tag in tags:
            qty = tags[tag]['count']
            allTags[tag] = allTags[tag] + qty if tag in allTags else qty

    # print('by links:\n\n', parsedLinks)
    linksTable = printSitesTable(parsedLinks)
    #print('\n\b - all tags:\n', allTags)
    tagsTable = printAllTagsTable(allTags)
    #writeResults('results/links', linksTable)
    writeCachedContent('results/tags', tagsTable)
    writeCachedContent('results/parsedLinks', linksTable)
            



if __name__=='__main__':
    main()
    #parseResult(readContentFromFile('./keep/documents/resultobject', False))