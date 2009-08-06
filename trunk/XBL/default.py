#!/usr/bin/python

# XBL Status -- a friends list for Xbox Live
# Copyright (c) 2008 Chris Hollenbeck
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import ConfigParser
from ConfigParser import NoOptionError
import os
import os.path
import re
import threading
import time
import urllib2

from LiveError import LiveError
from LiveConnect import LiveConnect
from LiveFriend import LiveFriend

# Default username and password
# There is no need to edit these in this version.  Use the Edit->Preferences
# menu item instead.
LIVE_LOGIN = "user@example.org"
LIVE_PASSWD = "password"

# Default file locations
SETTINGS_DIR = os.getcwd()
CONFIG_PATH = os.path.join(SETTINGS_DIR, "xblstatus.config")

# Default preferences
AUTO_CONNECT = False 
SHOW_OFFLINE_FRIENDS = True

class XBLStatus:
    def __init__(self, xbl, config_parser):
        self.xbLive = xbl
        self.configParser = config_parser
	
	#Glade loader here... modify
	#
	
        # set preferences
        self.autoConnect = AUTO_CONNECT
        self.showOffline = SHOW_OFFLINE_FRIENDS
        
        # this is set to True once the friends list has been updated
        self.updatedOnce = False
        
	try:
	    self.xbLive.connect()
	    print "connected???"
	except LiveError, e:
	    # TODO: add in error handling in LiveConnect to throw LiveErrors
	    print "Error message while connecting:", e.message
            return
            
         # update friends
        self.updateFriendsList()   
        

    def savePreferences(self):
        # create the sections if the file was not previously loaded
        if not self.configParser.has_section("auth"):
            self.configParser.add_section("auth")
        if not self.configParser.has_section("prefs"):
            self.configParser.add_section("prefs")            
        
        # set the options for authentication
        self.configParser.set("auth", "login", self.xbLive.username)
        self.configParser.set("auth", "password", self.xbLive.password)
        
        # set the options for preferences - values must be converted to strings
        self.configParser.set("prefs", "auto_connect", \
            str(self.autoConnect))
        self.configParser.set("prefs", "show_offline", \
            str(self.showOffline))
        self.configParser.set("prefs", "notification_enabled", \
            str(self.notificationEnabled))
        self.configParser.set("prefs", "notification_type", \
            str(self.notificationType))

        # write the file
        config_file = open(CONFIG_PATH, 'w')
        self.configParser.write(config_file)

    def updateFriendsList(self):
        friends = self.xbLive.liveFriends
        
        # regex for grabbing the friend's time offline
        # this matches a date (mm/dd/yy) or the number of hours/minutes ago
        offlineTime = "".join(["Last seen ", \
            "([0-9]{1,2}(\/[0-9]{1,2}\/[0-9]{1,2})? (hour|minute)?[s]?)"])
        offlineRegex = re.compile(offlineTime)

        # count online friends for the system tray tooltip
        friendsonline = 0

        keys = sorted(friends.keys())
        for k in keys:
            friend = friends[k]

            if friend.isOnline():
                friendsonline += 1
                # set a multi-line message to include 'Playing ...', etc.
                friendInfo = "".join([friend.gamerTag, '\n', \
                    friend.description])
                
                if friend.oldStatus != "Online":
                    self.updateTreeItem(friend, True, friendInfo)
                    
                    if self.notificationEnabled:
                        self.notification.notify("Online", friendInfo, \
                                                    friend.gamerPic)
                else:
                    if friend.descUpdated == True:
                        self.updateTreeItemDescription(friend, friendInfo)
                        
                        if self.notificationEnabled:
                            self.notification.notify("Online", friendInfo, \
                                                        friend.gamerPic)

            if friend.isAway():
                friendsonline += 1
                if friend.oldStatus != "Away":
                    # set a multi-line message to include 'Away'
                    friendInfo = "".join([friend.gamerTag, '\n', "Away"])
                    
                    self.updateTreeItem(friend, True, friendInfo)
                    
                    if self.notificationEnabled:
                        self.notification.notify("Away", friendInfo, \
                                                    friend.gamerPic)

            if friend.isBusy():
                friendsonline += 1
                if friend.oldStatus != "Busy":
                    # set a multi-line message to include 'Busy'
                    friendInfo = "".join([friend.gamerTag, '\n', "Busy"])
                
                    self.updateTreeItem(friend, True, friendInfo)
                    
                    if self.notificationEnabled:
                        self.notification.notify("Busy", friendInfo, \
                                                    friend.gamerPic)

            if friend.isPending():
                if friend.oldStatus != "Pending":
                    # set a multi-line message to include 'Pending'
                    friendInfo = "".join([friend.gamerTag, '\n', "Pending"])
                    
                    # treat the Pending friend the same way as 'Offline', i.e.
                    # don't show them when only viewing Online friends
                    self.updateTreeItem(friend, self.showOffline, friendInfo)
                    
                    # Don't notify for Pending friends

            if friend.isOffline():
                tmpStatus = "Offline"
                
                if friend.oldStatus != "Offline":                
                    m = re.match(offlineRegex, friend.description)
                    if m != None:
                        tmpStatus = "".join([tmpStatus, " - ", m.group(1)])

                    # set a multi-line message to include 'Offline'
                    friendInfo = "".join([friend.gamerTag, '\n', tmpStatus])
                    
                    self.updateTreeItem(friend, self.showOffline, friendInfo)
                    
                    # don't show a notification when starting the program
                    if self.notificationEnabled and self.updatedOnce:
                        self.notification.notify("Offline", friendInfo, \
                                                    friend.gamerPic)
                elif friend.descUpdated == True:
                    m = re.match(offlineRegex, friend.description)
                    if m != None:
                        tmpStatus = "".join([tmpStatus, " - ", m.group(1)])
                    
                    # set a multi-line message to include 'Offline'
                    friendInfo = "".join([friend.gamerTag, '\n', tmpStatus])
                    
                    self.updateTreeItem(friend, self.showOffline, friendInfo)
        
        print friendsonline
        self.updateTrayIcon(friendsonline)
        self.updatedOnce = True
        
        # needed for the timer to contine updating the friends list
        return True        
        
if __name__ == "__main__":
    # Create the initial connection
    # Note that all parameters are required
    xbLive = LiveConnect('mpauley73@hotmail.com', '4revenge', os.getcwd())
    xbLive.connect()
    friends = xbLive.liveFriends
    print friends