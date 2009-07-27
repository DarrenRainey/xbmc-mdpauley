
__plugin__ = "NFL Network Highlights"
__author__ = "MDPauley"
__url__ = ""
__version__ = "0.7.6"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

# Shared resources
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )
#load sqlite library
from pysqlite2 import dbapi2 as sqlite

#Does nfl.db exsist?
nfl_db_path = os.path.join( os.getcwd(), "nfl.db" )

# Create nfl.db if needed
#if ( not os.path.isfile( nfl_db_path ) ):
	
conn = sqlite.connect(nfl_db_path)
c = conn.cursor()
try:
	c.execute('create table nfl_videos (videoCMSID text, channelId text, headline text, pageURL text, caption text, runtime text, smallImage text)')
except conn.OperationalError, msg:
	print msg


def catInitial():
	addDir('Shows','http://www.nfl.com/ajax/videos?categoryId=featured', 10 , '')
	addDir('Teams','http://www.nfl.com/ajax/videos?categoryId=featured', 20 , '')
	addDir('Spotlight', 'http://nfl.com/ajax/videos?categoryId=nflFilms', 40, '')
	addDir('Events', 'http://nfl.com/ajax/videos?categoryId=events', 50, '')

def catShows():
	req = urllib2.Request('http://www.nfl.com/videos')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	code=re.sub('\r','',link)
	code=re.sub('\n',' ',code)
	code=re.sub('\t',' ',code)
	code=re.sub('  ','',code)
	code=re.sub('&#039;','\'',code)
	response.close()
	code=code.split('<li id=\"alt-nv-group-shows\" class=\"alt-nv-group\">');
	code=code[1].split('<li id=\"alt-nv-group-teams\" class=\"alt-nv-group\">');
	code=re.sub('<h3><a href=\"#\">Shows</a></h3> <div class=\"channel-content\"><div class=\"alt-nv-content-wrapper\"> <div class=\"video-nv-content bottom\"> <img src=\"http://static.nfl.com/static/content//public/image/videos/navigation/shows.png\" alt=\"\" /></div><div class=\"channels\"><ul>', '', code[0])
	p=re.compile('<li><a href=\"(.+?)\">(.+?)</a></li>')
	match=p.findall(code)
        for url, name in match:
        	url = re.sub('/videos/','',url)
                addDir(name, url, 500 , '')	

def catTeams():
	req = urllib2.Request('http://www.nfl.com/videos')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	code=re.sub('\r','',link)
	code=re.sub('\n',' ',code)
	code=re.sub('\t',' ',code)
	code=re.sub('  ','',code)
	code=re.sub('&#039;','\'',code)
	response.close()
	code=code.split('<li id=\"alt-nv-group-teams\" class=\"alt-nv-group\">');
	code=code[1].split('<li id=\"alt-nv-group-game-highlights\" class=\"alt-nv-group\">');
	code=re.sub('<h3><a href=\"#\">Shows</a></h3> <div class=\"channel-content\"><div class=\"alt-nv-content-wrapper\"> <div class=\"video-nv-content bottom\"> <img src=\"http://static.nfl.com/static/content//public/image/videos/navigation/shows.png\" alt=\"\" /></div><div class=\"channels\"><ul>', '', code[0])
	p=re.compile('<li><a href=\"(.+?)\">(.+?)</a></li>')
	match=p.findall(code)
        for url, name in match:
        	url = re.sub('/videos/','',url)
                addDir(name, url, 500 , '')

def catHighlights():
	req = urllib2.Request('http://www.nfl.com/videos')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	code=re.sub('\r','',link)
	code=re.sub('\n',' ',code)
	code=re.sub('\t',' ',code)
	code=re.sub('  ','',code)
	code=re.sub('&#039;','\'',code)
	response.close()
	code=code.split('<li id=\"alt-nv-group-game-highlights\" class=\"alt-nv-group\">');
	code=code[1].split('<li id=\"alt-nv-group-spotlight\" class=\"alt-nv-group\">');
	code=re.sub('<h3><a href=\"#\">Shows</a></h3> <div class=\"channel-content\"><div class=\"alt-nv-content-wrapper\"> <div class=\"video-nv-content bottom\"> <img src=\"http://static.nfl.com/static/content//public/image/videos/navigation/shows.png\" alt=\"\" /></div><div class=\"channels\"><ul>', '', code[0])
	p=re.compile('<li><a href=\"(.+?)\">(.+?)</a></li>')
	match=p.findall(code)
        for url, name in match:
        	url = re.sub('/videos/','',url)
                addDir(name, url, 500 , '')

def catSpotlight():
	req = urllib2.Request('http://www.nfl.com/videos')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	code=re.sub('\r','',link)
	code=re.sub('\n',' ',code)
	code=re.sub('\t',' ',code)
	code=re.sub('  ','',code)
	code=re.sub('&#039;','\'',code)
	response.close()
	code=code.split('<li id=\"alt-nv-group-spotlight\" class=\"alt-nv-group\">');
	code=code[1].split('<li id=\"alt-nv-group-events\" class=\"alt-nv-group\">');
	code=re.sub('<h3><a href=\"#\">Shows</a></h3> <div class=\"channel-content\"><div class=\"alt-nv-content-wrapper\"> <div class=\"video-nv-content bottom\"> <img src=\"http://static.nfl.com/static/content//public/image/videos/navigation/shows.png\" alt=\"\" /></div><div class=\"channels\"><ul>', '', code[0])
	p=re.compile('<li><a href=\"(.+?)\">(.+?)</a></li>')
	match=p.findall(code)
        for url, name in match:
        	url = re.sub('/videos/','',url)
                addDir(name, url, 500 , '')

def catEvents():
	req = urllib2.Request('http://www.nfl.com/videos')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	response = urllib2.urlopen(req)
	link=response.read()	
	code=re.sub('\r','',link)
	code=re.sub('\n',' ',code)
	code=re.sub('\t',' ',code)
	code=re.sub('  ','',code)
	code=re.sub('&#039;','\'',code)
	response.close()
	code=code.split('<li id=\"alt-nv-group-events\" class=\"alt-nv-group\">');
	code=code[1].split('<li id=\"alt-nv-group-all-videos\" class=\"alt-nv-group\">');
	code=re.sub('<h3><a href=\"#\">Shows</a></h3> <div class=\"channel-content\"><div class=\"alt-nv-content-wrapper\"> <div class=\"video-nv-content bottom\"> <img src=\"http://static.nfl.com/static/content//public/image/videos/navigation/shows.png\" alt=\"\" /></div><div class=\"channels\"><ul>', '', code[0])
	p=re.compile('<li><a href=\"(.+?)\">(.+?)</a></li>')
	match=p.findall(code)
        for url, name in match:
        	url = re.sub('/videos/','',url)
                addDir(name, url, 500 , '')

def listvideos(data):
	res=[]
	print 'http://www.nfl.com/ajax/videos/v2?channelId=' + data
	#this is where the fun starts, so we'll print some text here to
	print '**listvideos()'
		
        req = urllib2.Request('http://www.nfl.com/ajax/videos/v2?channelId=' + data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&#39;','',link)
        code2=re.sub('&amp;','&',code)
        response.close()
        p=re.compile('\"videoCMSID\":\"(.+?)\".+?,\"smallImage\":\"(.+?)\",\"videoDetailUrl\":\"(.+?)\"')
        match=p.findall(code2)
        for videoCMSID, smallImage, videoDetailUrl in match:   
		sql = "SELECT * from nfl_videos WHERE videoCMSID = '" + videoCMSID + "'"
		c.execute(sql)
		r = c.fetchone()
		if r == None:	
			req = urllib2.Request('http://www.nfl.com' + videoDetailUrl)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
			response = urllib2.urlopen(req)
			link=response.read()	
			code=re.sub('\r','',link)
			code=re.sub('\n',' ',code)
			code=re.sub('\t',' ',code)
			code=re.sub('  ','',code)
			code=re.sub('&amp;','&',code)
			response.close()       
			code=code.split('<!-- VIDEO DETAILS:')
			code=code[1].split('-->')
			p=re.compile('Story Headline:.(.+?)Caption:(.+?)Video.URL:(.+?)Run.Time:..+?\((.+?)\)')
			match2=p.findall(code[0])
			for Headline, Caption, VideoURL, RunTime in match2:
				Headline=re.sub('&amp;','&',Headline)
				Caption=re.sub('&amp;','&',Caption)
				res.append((Headline, Caption, VideoURL, RunTime))          	 
				sql = "insert into nfl_videos values ('" + videoCMSID + "', '" + data + "', '" + re.sub('\'', '', Headline) + "', '" + VideoURL + "', '" + re.sub('\'', '', Caption) + "', '" + RunTime + "', '" + smallImage + "')"
				c.execute(sql)
				conn.commit()
			for Headline, Caption, VideoURL, RunTime in match2:
				Headline=re.sub('&amp;','&',Headline)
				Caption=re.sub('&amp;','&',Caption)
				videoinfo = {'Title': Headline, "Date": "2009-01-01", 'Plot': Caption, 'Genre': 'Sports'}
				addLink(VideoURL, smallImage, Headline, videoinfo)
		elif r != None:
			res.append((r[2], r[4], r[3], r[5]))          	 
			headline=re.sub('&amp;','&',r[2])
			caption=re.sub('&amp;','&',r[4])
			videoinfo = {'Title': headline, "Date": "2009-01-01", 'Plot': caption, 'Genre': 'Sports'}
			addLink(r[3], r[6], headline, videoinfo)

	
def addLink(url, thumb, name, info):
	ok=True
	liz=xbmcgui.ListItem( name, iconImage="DefaultVideo.png", thumbnailImage= thumb )
	liz.setInfo( type="Video", infoLabels=info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

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
    catInitial()
elif mode==10:
    catShows()
elif mode==20:
    catTeams()
elif mode==30:
    catHighlights()
elif mode==40:
    catSpotlight()
elif mode==50:
    catEvents()
elif mode==500:
    listvideos(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))


c.close()
	
