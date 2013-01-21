import re,urllib,urllib2
url='http://btvguide.com/shows/list-type/new_shows'

def GET_HTML(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    html = link
    return html


html = GET_HTML(url)
r = re.compile(r'data-original="(.+?)".+?<h4>.+?<a href="(.+?)" title="(.+?)">.+?Watch Online', re.DOTALL|re.IGNORECASE).findall(html)
for image, showurl, title in r:
    print 'IMAGE: '+image+' SHOWURL: '+showurl+' TITLE: '+title
    #addon.add_directory({'mode': 'getlinks', 'url': showurl},{'title': title}, img = image)
        




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
