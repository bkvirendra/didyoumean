import os, urllib2, json, io, gzip, simplejson, sys, urllib, re
from bs4 import BeautifulSoup
from StringIO import StringIO

def getPage(url):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    return data

def didYouMean(q):
    q = str(str.lower(q)).strip()
    url = "http://www.google.com/search?q=" + urllib.quote(q)
    html = getPage(url)
    soup = BeautifulSoup(html)
    ans = soup.find('a', attrs={'class' : 'spell'})
    try:
        result = repr(ans.contents)
        result = result.replace("u'","")
        result = result.replace("/","")
        result = result.replace("<b>","")
        result = result.replace("<i>","")
        result = re.sub('[^A-Za-z0-9\s]+', '', result)
        result = re.sub(' +',' ',result)
    except AttributeError:
        result = -1
    return result

if __name__ == "__main__":
    response = didYouMean(sys.argv[1])
    print response