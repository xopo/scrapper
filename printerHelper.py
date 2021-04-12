from prettytable import PrettyTable

def objectCellDisplay(obj):
    if type(obj) == int:
        return obj
    if obj['count'] == 0 :
        return ''
    return 'c:%s%s' % (obj['count'], ('- m:%s' % obj['meta'] if 'meta' in obj and obj['meta'] > 0 else ''))

def objToString(results):
    return [objectCellDisplay(obj) for obj in results]

def countKeywords(kw):
    if not kw: return ''
    if isinstance(kw, str) and len(kw):
        return str(len(kw.split(',')))
    if isinstance(kw, list):
        return str(len(kw))

def sitesMetaTables(data):
    social = ['facebook', 'linkedin', 'youtube', 'instagram', 'twitter']
    socialCount = {}
    x = PrettyTable()
    y = PrettyTable()
    n = 0
    y.field_names = ['no', 'Site', 'Title', 'Keyword count', 'Description']
    x.field_names = ['no', 'Name', 'Internal Links', 'External Links', 'Domain'] + social
    for row in data:
        n = n + 1;
        socialData = [soc for soc in social if next((link for link in row['externalLinks'] if soc in link), None)]
        socialDataList = [(soc if soc in socialData else '') for soc in social]
        
        for soc in socialDataList: 
            if not soc in socialCount:
                socialCount[soc] = 0
            socialCount[soc] = socialCount[soc] + 1;

        x.add_row([
            n, row['name'], row['links'], len(row['externalLinks']), row['domain']] + socialDataList)
        y.add_row([ 
            n,
            row['name'].strip(),
            row['title'][:70].strip() if isinstance(row['title'], str) else '',
            countKeywords(row['keywords']),
            row['description'][:70].strip() if isinstance(row['description'], str) else '',
        ])
    x.add_row(['', '', '', '', ''] + [(socialCount[soc] if soc in socialCount else '') for soc in social])
    print(x);
    print(y);
    return [x.get_string(), y.get_string()];


def addSiteTag(oldCount, tags):
    for tag in tags:
        if not tag in oldCount:
            oldCount[tag] = 0
        if isinstance(tags[tag], int):
            oldCount[tag] = oldCount[tag] + tags[tag]
        else:
            qty = 1 if tags[tag]['count'] > 0 else 0
            oldCount[tag] = oldCount[tag] + qty
    return oldCount

    
def printSitesTagsTable(data):
    countSitesWithTag = {}
    try:
        n = 0
        x = PrettyTable()
        x.field_names = ['no', 'Site Name']  + [tag for tag in data[0]['tags']]
        for row in data:
            n = n + 1
            tagsFound = objToString(list(row['tags'].values()))
            countSitesWithTag = addSiteTag(countSitesWithTag, row['tags'])
            x.add_row([n, row['name']] + tagsFound)
        if len(countSitesWithTag):
            x.add_row(['', 'total sites'] + list(countSitesWithTag.values()) )
        print(x)
        return x.get_string() #border=False, padding_width=5)
    except Exception as e:
        print(e)
        print('print site table error', row)


def printAllTagsTable(data):
    x = PrettyTable()
    x.field_names = [key for key in data]
    x.add_row(objToString(list(data.values())))
    print(x)
    return x.get_string() #border=False, padding_width=5)