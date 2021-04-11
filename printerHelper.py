from prettytable import PrettyTable

def objectCellDisplay(obj):
    if type(obj) == int:
        return obj
    if obj['count'] == 0 or obj['meta'] == 0:
        return ''
    return 'c:%s - m:%s' % (obj['count'], obj['meta'])

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
    x.field_names = ['no', 'Name', 'External Links', 'Internal Links', 'Domain'] + social
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
    x.add_row(['', '', '', '', ''] + [socialCount[soc] for soc in socialCount if soc in social])
    print(x);
    print(y);
    return [x.get_string(), y.get_string()];

    
def printSitesTagsTable(data):
    try:
        n = 0
        x = PrettyTable()
        x.field_names = ['no', 'Site Name']  + [tag for tag in data[0]['tags']]
        for row in data:
            n = n + 1
            x.add_row([n, row['name']] + objToString(list(row['tags'].values())))
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