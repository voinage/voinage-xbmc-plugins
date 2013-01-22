import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,time,socket,string,os,shutil

#SET DIRECTORIES
local=xbmcaddon.Addon(id='plugin.video.Movie2k')

def delFAVS(url,title):
    Favs=re.compile('url="(.+?)",name="(.+?)"').findall(open('%s/resources/Favs'%local.getAddonInfo('path'),'r').read())
    if not str(Favs).find(title):
        xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]Movie2k[/COLOR][/B],[B][COLOR orange]"+title+"[/COLOR]not in Favourites.[/B],1000,"")")
    if len(Favs)<=1 and str(Favs).find(title):
        os.remove("%s/resources/Favs"%local.getAddonInfo('path'))
        xbmc.executebuiltin("Container.Refresh")
    if os.path.exists("%s/resources/Favs"%local.getAddonInfo('path')):
        for url,name in reversed(Favs):
            if title == name:
                Favs.remove((url,name))
                os.remove("%s/resources/Favs"%local.getAddonInfo('path'))
                for url,name in Favs:
                    try:
                        open("%s/resources/Favs"%local.getAddonInfo('path'),'a').write('url="%s",name="%s"'%(url,name))
                        xbmc.executebuiltin("Container.Refresh")
                        xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+title+"[/COLOR][/B],[B]Removed from Favourites[/B],1000,"")")
                    except: pass
    else: xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]Movie2k[/COLOR][/B],[B]You Have No Favourites to delete[/B],1000,"")")

bits = sys.argv[1].split(',')
print "BaseUrl= "+sys.argv[0]
url = bits[0].replace("[(u'",'').replace("'",'')
print "Url= "+url
title = bits[1].replace("'[B][COLOR green]",'').replace("[/COLOR][/B]')]",'').strip()
print "name= "+title

delFAVS(url.replace('[(',''),title.replace("'",'').replace(')]',''))
