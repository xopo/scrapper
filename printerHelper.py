from prettytable import PrettyTable

def printSitesTable(data):
    try:
        x = PrettyTable()
        x.field_names = ['Site Name', 'Links']  + [tag for tag in data[0]['tags']]
        for row in data:
            x.add_row([row['name'], row['links']] + list(row['tags'].values()))
        print(x)
    except:
        print('print site table error', data)


def printAllTagsTable(data):
    x = PrettyTable()
    x.field_names = [key for key in data]
    x.add_row(data.values())
    print(x)