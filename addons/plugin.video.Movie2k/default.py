import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,socket,os,shutil,urlresolver,string,xbmc,stat
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from metahandler import metahandlers

#SET DEFAULT TIMEOUT FOR SLOW SERVERS:
socket.setdefaulttimeout(300)# Bloody tvdb - slow or dead 

#SET DIRECTORIES & DB
local = xbmcaddon.Addon(id='plugin.video.Movie2k')
metafolder = xbmcaddon.Addon(id='script.module.metahandler')
metafolder.setSetting(id="meta_folder_location", value="%s/resources/Database/"%local.getAddonInfo('path'))
grab = metahandlers.MetaData(None,preparezip = False)
fanart = "%s/art/fanart.jpg"%local.getAddonInfo("path")
db = "%s/resources/Database/meta_cache/video_cache.db"%local.getAddonInfo("path")
addon = Addon('plugin.video.Movie2k', sys.argv)


def GRABMETA(name,type):
    if type == 'tvshow':
        meta = grab.get_meta(type,
                             name.replace('[B][COLOR green]','').replace('[/COLOR][/B]','').replace('*SUBTITLED*','').replace('-',' ').replace('... FOR DATING MY TEENAGE DAUGHTER',''), None, None, None, overlay=6)
        print "Tv Mode: %s"%name
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                      'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                      'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        if infoLabels['cover_url'] == '' : infoLabels['cover_url'] = "%s/art/folder.png"%local.getAddonInfo("path")
        
    elif type == 'movie':
        meta = grab.get_meta(type, name.replace('[B][COLOR green]','').replace('[/COLOR][/B]','').replace('*SUBTITLED*',''), None, None, None, overlay=6)
        print "Movie mode: %s"%name
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                      'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                      'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url']}
        if infoLabels['cover_url'] == '' : infoLabels['cover_url'] = "%s/art/folder.png"%local.getAddonInfo("path")
        
    elif type == 'episode': 
        blob = name.replace('[B][COLOR green]','').replace('[/COLOR][/B]','').replace('Season ','').replace('Episode ','').split('~')
        meta = grab.get_episode_meta(blob[0].strip(),None, int(blob[1].strip()), int(blob[2].strip()), overlay='6')
        print "Episode Mode: Name %s Season %s - Episode %s"%(blob[0].replace('[B][COLOR green]','').replace(' [/COLOR][/B]',''),blob[1],blob[2])
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                      'poster': meta['poster'],'season': meta['season'],'episode': meta['episode'],'backdrop_url': meta['backdrop_url']}
        if infoLabels['cover_url'] == '' : infoLabels['cover_url'] = "%s/art/folder.png"%local.getAddonInfo("path")
        
    elif type == None: 
        print "Plain Directory mode: %s"%name
        infoLabels = {'cover_url': '','title': name }
    return infoLabels

def FAVS():
    if os.path.exists("%s/resources/Favs"%local.getAddonInfo('path')):
        Favs=re.compile('url="(.+?)",name="(.+?)"').findall(open('%s/resources/Favs'%local.getAddonInfo('path'),'r').read())
        for url,name in Favs:
            addDir("[B][COLOR green]%s[/COLOR][/B]"%name,url,11,'',url.split('-')[-2],int(len(Favs)))
    else: xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]Movies2k[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")

def CATS():
    addDir("[B]SEARCH[/B]",'http://www.movie2k.to',12,"%s/art/search.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]MOVIES[/COLOR][/B]",'http://www.movie2k.to',1,"%s/art/movies.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]TV SHOWS[/COLOR][/B]",'http://www.movie2k.to',2,"%s/art/tvshows.png"%local.getAddonInfo("path"),None,1)
    addDir("[B]FAVOURITES[/B]",'http://www.movie2k.to',9,"%s/art/favourites.png"%local.getAddonInfo("path"),None,1)
    addDir("[B]RESOLVER SETTINGS[/B]",'http://www.movie2k.to',10,"%s/art/settings.png"%local.getAddonInfo("path"),None,1)
    
def MOVIES():
    addDir("[B][COLOR green]MOVIES ON THE CINEMA[/COLOR][/B]",'http://www.movie2k.to/index.php?lang=en',4,"%s/art/cinema.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]A-Z MOVIES[/COLOR][/B]",'http://www.movie2k.to/movies-all-1-1.html',5,"%s/art/atoz.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]GENRES[/COLOR][/B]",'http://www.movie2k.to/genres-movies.html',3,"%s/art/genre.png"%local.getAddonInfo("path"),None,1)

def TV():
    addDir("[B][COLOR green]FEATURED TV SHOWS[/COLOR][/B]",'http://www.movie2k.to/tvshows_featured.php',4,"%s/art/featured.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]A-Z TV SHOWS[/COLOR][/B]",'http://www.movie2k.to/tvshows-all.html',5,"%s/art/atoz.png"%local.getAddonInfo("path"),None,1)
    addDir("[B][COLOR green]GENRES[/COLOR][/B]",'http://www.movie2k.to/genres-tvshows.html',3,"%s/art/genre.png"%local.getAddonInfo("path"),None,1)

def AtoZ(url):
    cat = re.compile('/(.+?)-all').findall(url)[0]
    for i in string.ascii_uppercase: addDir(i,'http:/%s-all-%s-1.html'%(cat,i),7,"%s/art/Alphabet-%s.png"%(local.getAddonInfo("path"),i),None,26)
    addDir('#','http:/%s-all-1.html'%cat,7,"%s/art/0to9.png"%local.getAddonInfo("path"),None,1)

def FEAT(url):
    links=[]
    html = net().http_GET(url).content
    bits = re.compile('<div style="float:left"><a href="(.+?)"><img src=".+?" border=0 width=105 height=150 alt="(.+?)"').findall(html)
    if not bits: bits = re.compile('<div style="float:left"><a href="(.+?)" ><img src=".+?" border=0 style=".+?" alt="watch (.+?) online for free"').findall(html)
    for i in range(0,len(bits)):
        links.append((bits[i][1],"http://www.movie2k.to/%s"%bits[i][0]))
    for name,burl in links:
        if url.find('tvshows')>0:
            addDir("[B][COLOR green]%s[/COLOR][/B]"%name.replace('M.D.','').encode('ascii','ignore').replace('\xc3\xa9','e').upper(),burl,11,'','tvshow',int(len(links)))
        else: addDir("[B][COLOR green]%s[/COLOR][/B]"%name.encode('ascii','ignore').replace('\xc3\xa9','e').upper(),burl,8,'','movie',int(len(links)))

def SEARCH():
    keyb = xbmc.Keyboard('', '[B][COLOR green]SEARCH[/COLOR][/B] MOVIE2K');keyb.doModal()
    if (keyb.isConfirmed()):
        values = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Origin':'http://www.movie2k.to',
              'Referer':'http://www.movie2k.to/movies.php?list=search','Cookie':'onlylanguage=en'}
        html = net().http_POST('http://www.movie2k.to/movies.php?list=search',{'search': keyb.getText()},values,compression=False).content.replace('(TVshow)','').replace('(US)','US')
        linkage = re.compile('<TD width="550" id="tdmovies">.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html.replace('&#xC6;','Ae'))
        if not linkage: linkage = re.compile('<TD id="tdmovies" width="538"><a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html.replace('&#xC6;','Ae'))
        for url,name in linkage:
            try:
                if url.split('-')[-2] == 'movie':
                    addDir("[B][COLOR green]%s[/COLOR][/B]"%name.strip().replace('\t','').encode('ascii','ignore').upper(),"http://www.movie2k.to/%s"%url,8,'',url.split('-')[-2],int(len(linkage)))
                else: addDir("[B][COLOR green]%s[/COLOR][/B]"%name.strip().replace('1-800-','').replace('\t','').encode('ascii','ignore').upper(),"http://www.movie2k.to/%s"%url,11,'',url.split('-')[-2],int(len(linkage)))
            except: pass

def SEASONS(url,name):
    try:
        title = re.compile(r'www.movie2k.to-(.+?)-watch').findall(url.replace('/','-'))[0]
        html = net().http_GET(url,{'Cookie':'onlylanguage=en'}).content
        seasons = re.compile('<OPTION value="[^a-zA-Z]+">Season (.+?)</OPTION>').findall(html.replace(' selected','').replace('\t',''))
        cover = grab.get_seasons(name.replace('[B][COLOR green]','').replace('[/COLOR][/B]','').replace('*SUBTITLED*',''), None, seasons, overlay=6)
        covers= re.compile("'cover_url': '(.+?)',").findall(str(cover))
        for i in range(0,len(seasons)):
            addDir("%s ~ Season %s"%(name,seasons[i].replace('\t','').encode('ascii','ignore').strip()),url,6,covers[i],None,int(len(seasons)))
    except:
        html = net().http_GET(url,{'Cookie':'onlylanguage=en'}).content
        redirect = re.compile('<TD id="tdmovies" width="538"><a href="(.+?)">',re.DOTALL).findall(html.replace('\t',''))
        link="http://www.movie2k.to/%s"%re.compile('<TD id="tdmovies" width="538"><a href="(.+?)">',re.DOTALL).findall(net().http_GET("http://www.movie2k.to/%s"%redirect[0],{'Cookie':'onlylanguage=en'}).content)[0]
        SEASONS(link,name)
        
def EPS(url,name):
    compare = name.split('~')
    html = net().http_GET(url).content
    episodes = re.compile('<FORM name="(.+?)">\n.+?<SELECT name="episode" style=".+?">\n.+?<OPTION></OPTION>\n(.+?)</SELECT>',re.DOTALL).findall(html.replace('seasonform',compare[1].strip()).replace('episodeform','Season '))
    for i in range(0,len(episodes)):
        if compare[1].strip() == episodes[i][0]:
            eps=re.compile('<OPTION value="(.+?)">(.+?)</OPTION>').findall(episodes[i][1].replace(' selected',''))
    for url,title in eps:
        addDir("%s ~ %s"%(name,title),"http://www.movie2k.to/%s"%url,8,'','episode',int(len(eps)))

def SCAN(url,name):
    if name == '[B][COLOR green]ADULT[/COLOR][/B]':
        content = local.getSetting("Adult genre Password")
        if content == '':
            dialog = xbmcgui.Dialog()
            dialog.ok("[B][COLOR red]ADULT[/COLOR][/B]", "PASSWORD NOT SET")
            local.openSettings()
        keyb = xbmc.Keyboard('', '[B][COLOR red]ENTER ADULT PASSWORD[/COLOR][/B]');keyb.doModal()
        if (keyb.isConfirmed()):
            if content != keyb.getText():
                url="http://www.movie2k.to/"
                addDir("[B][COLOR red]~ CONTENT BLOCKED ~ [/COLOR][/B]","http://www.movie2k.to/",None,'',None,1)
            else: pass
    nextp=url.split('-')
    html = net().http_GET(url,{'Cookie':'onlylanguage=en'}).content
    linkage = re.compile('<TD width="550" id="tdmovies">.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html.replace('&#xC6;','Ae'))
    if not linkage: linkage = re.compile('<TD id="tdmovies" width="538"><a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html.replace('&#xC6;','Ae'))
    try:
        if url.find('tvshows')<1 and linkage:  addDir('[B][COLOR orange]NEXT PAGE >>>[/COLOR][/B]',"%s-%s-%s-%s.html"%(nextp[0],nextp[1],nextp[2],
                                                                                                   str(int(nextp[-1].replace('.html',''))+1)),7,"%s/art/next.png"%local.getAddonInfo("path"),None,1)
        else: addDir('[B][COLOR green]END[/COLOR][/B][B] ~ BACK TO THE FIRST PAGE >>>[/B]',"%s-%s-%s-1.html"%(nextp[0],nextp[1],nextp[2]),7,"%s/art/back.png"%local.getAddonInfo("path"),None,1)
    except: pass
    if linkage and url.find('tvshows')>0:
        print "TV SCAN MODE"
        for url,name in linkage:
            addDir("[B][COLOR green]%s[/COLOR][/B]"%name.strip().replace('1-800-','').replace('\t','').encode('ascii','ignore').upper(),"http://www.movie2k.to/%s"%url,11,'','tvshow',int(len(linkage)))
    else:
        print "MOVIE SCAN MODE"
        for url,name in linkage:
            addDir("[B][COLOR green]%s[/COLOR][/B]"%name.strip().replace('\t','').encode('ascii','ignore').upper(),"http://www.movie2k.to/%s"%url,8,'','movie',int(len(linkage)))

def INDEX(url):
    html = net().http_GET(url,{'Cookie':'onlylanguage=en'}).content
    index = re.compile('<TD id="tdmovies" width=".+?"><a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html.replace('\t',''))
    if not index: index = re.compile('<TD width="550" id="tdmovies">.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
    if url.find('/genres-')>0:
        print "GENRE MODE"
        for url,name in index:
            addDir("[B][COLOR green]%s[/COLOR][/B]"%name.strip().encode('ascii','ignore').upper(),
                   'http://www.movie2k.to/%s-%s-%s-1.html'%(url.split('-')[0],url.split('-')[1],
                                                            url.split('-')[2]),7,"%s/art/%s.png"%(local.getAddonInfo("path"),name),None,int(len(index)))
    else:
        if url.find('/movies-genre-')>0:
            print "MOVIE SCAN MODE"
            for url,name in index:
                addDir("[B][COLOR green]%s[/COLOR][/B]"%name.encode('ascii','ignore').upper(),'http://www.movie2k.to/%s'%url,8,"%s/art/latest.png"%local.getAddonInfo("path"),'movie',int(len(index)))
        else:
            print "TV SCAN MODE"
            for url,name in index:
                addDir("[B][COLOR green]%s[/COLOR][/B]"%name.encode('ascii','ignore').upper(),'http://www.movie2k.to/%s'%url,11,"%s/art/latest.png"%local.getAddonInfo("path"),'tvshow',int(len(index)))
    
def RESOLVE(url,name):
    sources=[]
    title = name.split('~')[0]
    sources=[]
    html = net().http_GET(url,{'referer': url}).content.replace('&nbsp;','').replace('\\','')
    links = re.compile(r'<a href="(.+?)".+?img border=0 style=".+?" src=".+?" alt=".+?" title=".+?" width="16">(.+?)</a>').findall(html)
    for i in range(0,len(links)):
        addDir(links[i][1].upper(),"http://www.movie2k.to/%s"%links[i][0],13,"%s/art/video.png"%local.getAddonInfo("path"),None,int(len(sources)))

def PLAY(url,name):
    html = net().http_GET(url).content.replace('scrolling="no"','').replace('width=100% height=320px frameborder="0"  ','')
    link=re.compile('<iframe width=.+?src="(.+?)".+?<',re.DOTALL).findall(html)
    if not link: link = re.compile('<a target="_blank" href="(.+?)"><img border=0').findall(html)
    if not link: link = re.compile('<iframe src="(.+?)"').findall(html)
    if name.strip() == 'VIDEOWEED': stream=urlresolver.resolve(link[0].replace('file','video'))
    else: stream=urlresolver.resolve(link[0])
    liz=xbmcgui.ListItem(label = name,label2 = name, iconImage="%s/art/video.png"%local.getAddonInfo("path"), thumbnailImage = "%s/art/video.png"%local.getAddonInfo("path") )
    liz.setInfo( type="Video", infoLabels = {'title' : name}); liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable', 'true'); addon.resolve_url(stream)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=stream,listitem=liz)
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,type,total):
    ok=True
    if local.getSetting("Metadata ON/OFF") == "true": infoLabels = GRABMETA(name,type)
    else: infoLabels = {'cover_url': "%s/art/folder.png"%local.getAddonInfo("path"),'title': name }
    if type == None: img = iconimage
    else: img = infoLabels['cover_url']
    if img.find('imdb')>0: img = "%s/art/folder.png"%local.getAddonInfo("path")
    args=[(url,infoLabels['title'])]
    script1="%s/resources/addFavs.py"%local.getAddonInfo('path')
    script2="%s/resources/delFavs.py"%local.getAddonInfo('path')
    Commands=[('Add to [B][COLOR orange]Movie2k[/COLOR][/B] Favourites',"XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ('Remove from [B][COLOR orange]Movie2k[/COLOR][/B] Favourites',"XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
    liz=xbmcgui.ListItem(name, iconImage = "%s/art/folder.png"%local.getAddonInfo("path"), thumbnailImage = img)
    liz.addContextMenuItems( Commands )
    liz.setProperty('fanart_image', fanart)
    if local.getSetting("Allow Fanart Backgrounds") == "true": 
        try:
            liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        except: pass
    liz.setInfo( type="Video", infoLabels = infoLabels );ok=True
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=total)
    return ok 
       
params=get_params()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    CATS()
elif mode==1:
    MOVIES()
elif mode==2:
    TV()
elif mode==3:
    INDEX(url)
elif mode==4:
    FEAT(url)
elif mode==5:
    AtoZ(url)
elif mode==6:
    EPS(url,name)
elif mode==7:
    SCAN(url,name)
elif mode==8:
    RESOLVE(url,name)
elif mode==9:
    FAVS()
elif mode==10:
    urlresolver.display_settings()
elif mode==11:
    SEASONS(url,name)
elif mode==12:
    SEARCH()
elif mode==13:
    PLAY(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]),succeeded=True)

