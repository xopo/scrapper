from os.path import isfile, join

def readContentFromFile(filename, split=True): 
    if not isfile(filename): return ''
    with open(filename) as f:
        content = f.read()
        if (content):
            return content.split('\n') if split else content
        print('\n\n\t\t\t - error reading %s', filename)


def parseContentAskeydObject(content, removeDashComment=True):
    result = {'all': []}
    key = ''
    for line in content:
        line = line.strip()
        if len(line) == 0 or line[0] =='~': 
            continue
        elif line[0] == '#':
            key = line
            if key in result:
                print('key %s already in result' % key)
            else: 
                result[key] = []
        elif line == '@stop':
            break
        else:
            # some lines have comment, remove them
            if removeDashComment: 
                line = line.split(' - ')[0].strip()
            result[key] = result[key] + [line]
            result['all'] = result['all'] +  [line]
    return result

def getListOfTags(): 
    tags = readContentFromFile('./tags')
    return parseContentAskeydObject(tags)
        

def getListOfSites(): 
    sites = readContentFromFile('./sites')
    return parseContentAskeydObject(sites)


def getPageMockContent(): 
    with open('./tests/primaria.html') as f:
        content = f.read()
        if (content):
            return content;


def writeCachedContent(filewithpath, content):
    with open(filewithpath, 'w+') as f:
        try:
            f.write(content)
        except Exception(e):
            filewithpath.write(e)