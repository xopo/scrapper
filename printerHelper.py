from prettytable import PrettyTable

def objectCellDisplay(obj):
    if type(obj) == int:
        return obj
    if obj['count'] == 0 or obj['meta'] == 0:
        return ''
    return 'c:%s - m:%s' % (obj['count'], obj['meta'])

def objToString(results):
    return [objectCellDisplay(obj) for obj in results]
    
def printSitesTable(data):
    try:
        x = PrettyTable()
        x.field_names = ['Site Name', 'Links', 'ExternalLinks']  + [tag for tag in data[0]['tags']]
        for row in data:
            x.add_row([row['name'], row['links'], len(row['externalLinks'])] + objToString(list(row['tags'].values())))
        print(x)
        return x.get_string() #border=False, padding_width=5)
    except:
        print('print site table error', data)


def printAllTagsTable(data):
    x = PrettyTable()
    x.field_names = [key for key in data]
    x.add_row(objToString(list(data.values())))
    print(x)
    return x.get_string() #border=False, padding_width=5)