
__plugin__ = "FoodNetwork"
__author__ = "MDPauley"
__url__ = ""
__version__ = "0.0.5"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

def catsInitial():
        req = urllib2.Request('http://www.foodnetwork.com/video-library/index.html')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()	
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        response.close()	
	code=code.split('<h3>Video Channels</h3>')
	p=re.compile('<h4>\"(.+?)\"*Full Episodes</h4><div id=\"chnl-(.+?)\" class=\"crslFour92 crsl-w\">')
	match=p.findall(code[1])
        for showname, showcode in match:
                showname=re.sub('\"','',showname)
                addDir(showname,'http://www.foodnetwork.com/food/channel/xml/0,,' + showcode + ',00.xml', 50 , '')	
	        
"""
	INDEX()
	Parses the data to create the filelist
"""
def listvideos(data):
	res=[]
	#this is where the fun starts, so we'll print some text here to
	#locate this section of code in the boxee debug logs.
	print '**listvideos()'	
        req = urllib2.Request(data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&#39;','',link)
        code=re.sub('&amp;','&',code)
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        response.close()
        p=re.compile('<clipName><\!\[CDATA\[(.+?)\]\]></clipName><length>(.+?)</length><sourceNetwork>(.+?)</sourceNetwork><videoUrl><\!\[CDATA\[(.+?)\]\]></videoUrl><thumbnailUrl><\!\[CDATA\[(.+?)\]\]></thumbnailUrl><abstract><\!\[CDATA\[(.+?)\]\]></abstract>')
        match=p.findall(code)
        for mainTitle, thumbRunTime, network, filePath, controlPanelImage, captionBlurb in match:
                filePath=re.sub('http','mms',filePath)
                res.append((filePath, mainTitle, controlPanelImage, mainTitle, captionBlurb, thumbRunTime))     
        for mainTitle, thumbRunTime, network, filePath, controlPanelImage, captionBlurb in match:
		filePath=re.sub('http','mms',filePath)
		videoinfo = {'Title': mainTitle, "Date": "2009-01-01", 'Plot': captionBlurb, 'Genre': 'Food', 'Duration': thumbRunTime}
                addLink(filePath + '?MSWMExt=.asf', controlPanelImage, mainTitle, videoinfo)

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
