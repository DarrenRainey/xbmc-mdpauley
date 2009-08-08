
__plugin__ = "Bang Bros Network"
__author__ = "MDPauley"
__url__ = ""
__version__ = "0.7.5"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

def catsInitial():
	print '**catsInitial()'	
        req = urllib2.Request('http://bangbros.com/t1/pps=bbonet/websites')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()	
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        response.close()	
	p=re.compile('<table width=.+?cellpadding=.+?cellspacing=.+?><tr>.+?<td valign=top><a href=\"(.+?)\" title=\"(.+?)\"><img class=\".+?\"src=\"(.+?)\" width=.+?height=.+?alt=\".+?\"></a></td></tr><tr>.+?<td valign=\"top\">.+?<div class=\".+?\"><b><a href=\"(.+?)\" class=\".+?\" title=\".+?\">(.+?)</a></b><br>(.+?)</div>.+?</td></tr>.+?</table>')
	match=p.findall(code)
        for var1, var2, var3, var4, var5, var6 in match:
                addDir(var2,'http://bangbros.com/t1/pps=bbonet/' + var1, 50 , var3)	
	        
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
        p=re.compile('<div class=\"res_shoot\"><a href=\"(.+?)\"><img class=\"img_href_1\" src=\"(.+?)\" width=.+?height=.+?border.+?></a><span class=\"res_shoot_descr\"><a href=\"(.+?)\" class=\"res_shoot_title\"><b>(.+?)</b></a> <br> <span class=\"gp2\">Added:.(.+?)</span> <br> <span class=\"gp2\">Rating:.(.+?)</span> </span> </div>')
        match=p.findall(code)
        for var1, var2, var3, var4, var5, var6 in match:
        	var3=re.sub('intro','trailers',var3)
        	req = urllib2.Request('http://bangbros.com/t1/pps=bbonet/' + var3)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
		response = urllib2.urlopen(req)
		link2=response.read()
		code2=re.sub('&#39;','',link2)
		code2=re.sub('&amp;','&',code2)
		code2=re.sub('\r',' ',code2)
		code2=re.sub('\n',' ',code2)
		code2=re.sub('\t',' ',code2)
		code2=re.sub('   ',' ',code2)
		code2=re.sub('  ',' ',code2)
		response.close()
		p=re.compile('clip:.+?{.+?url: \'(.+?)\',')
		match2=p.findall(code2)
		for var7 in match2:
			videoinfo = {'Title': var4, "Date": "2009-01-01", 'Plot': var4, 'Genre': 'adult'}
			addLink(var7, var2, var4, videoinfo)

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
