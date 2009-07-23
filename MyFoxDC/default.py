
__plugin__ = "MyFoxDC Live"
__author__ = "MDPauley"
__url__ = ""
__version__ = "0.7.5"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

def catsInitial():
        req = urllib2.Request('http://www.myfoxdc.com/subindex/live_video/news_now')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()	
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        response.close()	
	p=re.compile('<iframe src=\'(.+?)\' frameBorder=\'0\'> </iframe>')
	match=p.findall(code)
        for url in match:        
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
		response = urllib2.urlopen(req)
		link=response.read()	
		code=re.sub('\r','',link)
		code=re.sub('\n',' ',code)
		code=re.sub('\t',' ',code)
		code=re.sub('  ','',code)
		response.close()	
        	p=re.compile('<param name=\'fileName\' value=\"(.+?\?bkup.+?)\"> <param name=\'animationatStart\' value=\'true\'>')
        	match2=p.findall(code)
        	for url2 in match2:
			videoinfo = {'Title': 'MyFoxDC Live'}
            		addLink(url2, 'http://media2.myfoxdc.com/graphics/logos_myfoxdc/png24_myfoxdc149x74.png', 'Watch MyFoxDC Live', videoinfo)
	        
"""
	addLink()
	this function simply adds a media link to boxee's current screen
"""
def addLink(url, thumb, name, info):
	ok=True
	liz=xbmcgui.ListItem( name, iconImage="DefaultVideo.png", thumbnailImage= thumb )
	liz.setInfo( type="Video", infoLabels=info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

"""
	addDir()
	this function simply adds a directory link to boxee's current screen
"""
def addDir(name,url,mode,iconimage, plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	if plot:
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

"""
	getParams()
	grab parameters passed by the available functions in this script
"""
def getParams():
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

#grab params and assign them if found
params=getParams()
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

#check $mode and execute that mode
if mode==None or url==None or len(url)<1:
    print "CATEGORY INDEX : "
    catsInitial()
elif mode==50:
    listvideos(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
