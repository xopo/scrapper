#!/usr/bin/env python3
from pprint import pprint
import json


from fileHelpers import isfile, join, getListOfTags, getListOfSites, readContentFromFile, writeCachedContent
from printerHelper import printSitesTable, printAllTagsTable
from htmlParser import hashFromString, getMetaData, getSiteName, getSiteContent, getSiteNavigation, extractTagsFromPage

# use a salt to cache result. if update is changed data will be gathered anew
update = 3

# add to the list
def analyzeContent(sites, tags):
    results = {}
    for site in sites['all']: 
        siteContent = getSiteContent(site)
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


def main(): 
    ''' get sites and tags from the lists'''
    tags = getListOfTags()
    sites = getListOfSites()
    searchEntity = hashFromString(json.dumps([ tags,  sites,  update]))
    resultFile = join('./results', searchEntity)
    print(resultFile)
    if isfile(resultFile):
        jsonResult = readContentFromFile(resultFile, False)
        result = json.loads(jsonResult)
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
            links = target['links'] # [:10] # take first 10
            counter = -1 # so we start from 0
            while counter < 50:
                counter = counter + 1;        #for idx,adr in enumerate(links):
                if len(links) <= counter:
                    counter = 51
                    break
                adr = links[counter]
                content = getSiteContent(adr['link'])
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
        # save it for later change in parse data
        writeCachedContent(resultFile, json.dumps(results))

    parseResult(result)

def countTags(data): 
    tags = {}
    for key in data: 
        for tag in data[key]['tags']:
            if not tag in tags:
                tags[tag] = 0
            try:
                qty = data[key]['tags'][tag]['count']
            except:
                print('some error getting qty', data[key]['tags'][tag])
                qty = 0 
            tags[tag] = tags[tag] + qty if tag in tags else qty
    return tags;



def parseResult(data):
    allTags = {}
    pretyObject = []
    parsedLinks = []
    for key in data: 
        entity = data[key]
        tags = countTags(entity['data'])
        parsed = {
            'name': entity['name'],
            'links': len(entity['links']),
            'tags' : tags,
        }
        parsedLinks.append(parsed)
        for tag in tags:
            qty = tags[tag]
            allTags[tag] = allTags[tag] + qty if tag in allTags else qty

    # print('by links:\n\n', parsedLinks)
    linksTable = printSitesTable(parsedLinks)
    #print('\n\b - all tags:\n', allTags)
    tagsTable = printAllTagsTable(allTags)
    #writeResults('results/links', linksTable)
    writeResults('results/tags', tagsTable)

            



if __name__=='__main__':
    main()
    #parseResult(readContentFromFile('./keep/documents/resultobject', False))