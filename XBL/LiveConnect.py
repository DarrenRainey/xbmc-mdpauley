#!/usr/bin/python

# LiveConnect -- a class for connecting to live.xbox.com
# Copyright (c) 2008-2009 Chris Hollenbeck
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

import BaseHTTPServer
import cookielib
#import hashlib
import os
import os.path
import re
import sys
import urllib2

from BeautifulSoup import BeautifulSoup, SoupStrainer
import ClientForm

from LiveError import LiveError
from LiveFriend import LiveFriend

class LiveConnect:

    def __init__(self, uname, passwd, setDir):
        self.username = uname
        self.password = passwd
        self.settingsDir = setDir
        self.cacheDir = os.path.join(setDir, "cache")
        self.cookieFile = os.path.join(setDir, ".cookie")
        self.liveFriends = {}
        self.friendsURL = "http://live.xbox.com/en-US/profile/Friends.aspx"
        self.friendsPage = None
        self.friendsMessengerURL = "http://live.xbox.com/en-us/profile/FriendsMessengerTab.aspx"
        
        # Check that the settings directory exists
        if os.path.exists(self.settingsDir) == False:
            # create the directory
            os.mkdir(self.settingsDir)

        # Check that the cache directory exists
        if os.path.exists(self.cacheDir) == False:
            # create the directory
            os.mkdir(self.cacheDir)

        # Hold the cookies
        #   Note that MozillaCookieJar is now used instead of LWPCookieJar,
        #   which has a bug with cookie years of 2038 or greater on 32-bit
        #   systems.
        self.cookiejar = cookielib.MozillaCookieJar()
        
        # Load the cookies if they already exist
        if os.path.isfile(self.cookieFile):
            try:
                self.cookiejar.load(self.cookieFile)
            except cookielib.LoadError:
                print "Old LWPCookie found, replacing with MozillaCookie"
                os.remove(self.cookieFile)
        
        # Install the cookie jar
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        urllib2.install_opener(self.opener)
                
        return
        
    def connect(self):
        # Start looking up pages ...
        # TODO: need to add in some checks to see if there is an error with
        # the Live site
        request = urllib2.Request(self.friendsURL)
        try:
            response = urllib2.urlopen(request) 
        except urllib2.URLError, e:
            if hasattr(e,'reason'):
                print "Error connecting to the initial Live login page."
                print "Reason:", e.reason
                errorMsg = "".join(["Error connecting to initial login page:\n",\
                    e.reason[1]])
                raise LiveError(errorMsg)
            elif hasattr(e,'code'):
                print "Error with the initial request to the Live login page."
                httpError = \
                    BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                print "Error:", e.code, httpError
                errorMsg = "".join(["Error requesting initial login page:\n",
                    httpError])
                raise LiveError(errorMsg)
            else:
                print "Unknown error with the initial request to the Live login."
                raise LiveError("Unknown error connecting to initial login.")
            
        
        # If the friend's page is not the current one, this means the cookie has 
        # not been set and the user must be logged in
        if response.geturl() != self.friendsURL:
            forms = ClientForm.ParseResponse(response, backwards_compat=False)
            response.close()

            form = forms[0]

            # Set credentials
            form["login"] = self.username
            form["passwd"] = self.password
        
            # Save username/password for session
            form["LoginOptions"] = ["3"]
                        
            # Set variables from the javascript
            control = form.find_control("PwdPad", type="hidden")
            control.readonly = False
        
            # Full variable is "IfYouAreReadingThisYouHaveTooMuchFreeTime"
            # Calculate PwdPad by taking the last 'n' characters off, where
            # 'n' is the length of the password
            pwdPad = "IfYouAreReadingThisYouHaveTooMuchFreeTime"
            form["PwdPad"] = pwdPad[0:len(pwdPad)-len(self.password)]

            # Submit login form
            request2 = form.click()
            try:
                response2 = urllib2.urlopen(request2)
            except urllib2.URLError, e:
                if hasattr(e,'reason'):
                    print "Error connecting to the login refresh page."
                    print "Reason:", e.reason
                    errorMsg = "".join(["Error connecting to login refresh page:\n",
                        e.reason[1]])
                    raise LiveError(errorMsg)
                elif hasattr(e,'code'):
                    print "Error requesting refresh page."
                    httpError = \
                        BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                    print "Error:", e.code, httpError
                    errorMsg = "".join(["Error requesting login refresh page:\n",
                        httpError])
                    raise LiveError(errorMsg)
                else:
                    print "Unknown error with the request to login refresh."
                    raise LiveError("Unknown error connecting to login refresh.")
        
            # Grab the forms from the refresh page.  The one of interest
            # is the first form.
            forms2 = ClientForm.ParseResponse(response2, backwards_compat=False)
            response2.close()
            form2 = forms2[0]
        
            # Finally, 'submit' the hidden form to access the friends page
            request3 = form2.click()
            
            # Load the original friends page to complete the login
            try: 
                response3 = urllib2.urlopen(request3)
                response3.close()
            except urllib2.URLError, e:
                if hasattr(e,'reason'):
                    print "Error connecting to the friends page."
                    print "Reason:", e.reason
                    errorMsg = "".join(["Error connecting to the friends page:\n",
                        e.reason[1]])
                    raise LiveError(errorMsg)
                elif hasattr(e,'code'):
                    print "Error with the request to the friends page."
                    httpError = \
                        BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                    print "Error:", e.code, httpError
                    errorMsg = "".join(["Error requesting friends page:\n",
                        httpError])
                    raise LiveError(errorMsg)
                else:
                    print "Unknown error with the request to the friends page."
                    raise LiveError("Unknown error connecting to friends page.")
        
            # At this point, the user is logged in and should remain that way
            # as long as the session cookie remains valid
        
            # Save the cookies
            # TODO: need some error handling
            self.cookiejar.save(self.cookieFile)

        # Now refresh the Live Messenger friends page
        requestFriends = urllib2.Request(self.friendsMessengerURL)
        self.refreshFriends(requestFriends)
        
        return

    def refresh(self):
        """ Refresh the Friends page """
        requestFriends = urllib2.Request(self.friendsMessengerURL)
        self.refreshFriends(requestFriends)
        
        return

    def refreshFriends(self, request):
        # Refresh the friends page using the given request since we should now
        # be logged in for the session
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if hasattr(e,'reason'):
                print "Error connecting to the friends page for refresh."
                print "Reason:", e.reason
                errorMsg = "".join(["Error connecting to the friends page for refresh:\n",
                    e.reason[1]])
                raise LiveError(errorMsg)
            elif hasattr(e,'code'):
                print "Error with the request to the friends page for refresh."
                httpError = \
                    BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
                print "Error:", e.code, httpError
                errorMsg = "".join(["Error requesting friends page for refresh:\n",
                    httpError])
                raise LiveError(errorMsg)
            else:
                print "Unknown error refreshing the friends page."
                raise LiveError("Unknown error refreshing the friends page.")
        
        # Save the HTML of the friends page
        self.friendsPage = response.read()
        response.close()
        
        # Parse all the friends and save them in the dictionary self.liveFriends
        self.parseFriendsPage(self.friendsPage)
        
        return

    def parseFriendsPage(self, friendsPage):
        ######
        # TODO: add error handling
        # TODO: should this return friends instead?
        ######

        soup = BeautifulSoup(''.join(friendsPage))

        # Grab all of the gamertags (status/descriptions are also found in here)
        allGamertags = soup.findAll("td", "XbcFriendsListWPGamertagCell")

        # Grab all of the gamerpictures
        # NOTE: The NXE update caused the image locations to change from tiles.xbox.com to
        # either avatar.xboxlive.com (new avatars) or image.xboxlive.com (old gamerpictures)
        allGamerpictures = soup.findAll("img", src=re.compile('(avatar|image).xboxlive.com'))

        # regex for grabbing the current status from the description
        statusRegex = re.compile("Status: (.*)")

        # Save all the friends into self.liveFriends
        i = 0
        for foundTag in allGamertags:
            # the gamertag is beneath <p>, <strong>, and <a href=...> tags
            gTag = foundTag.contents[0].contents[0].contents[0].contents[0]

            gPicURL =  allGamerpictures[i].attrs[2][1]
            
            # extract the status (online, offline, etc) and set the description
            tmpDesc = foundTag.contents[0].contents[2]
            m = re.match(statusRegex, tmpDesc)
            if m != None:
                gPres = m.group(1)
                gDesc = m.group(1)
            else:
                gPres = "Unknown"
                gDesc = "Unknown"
            
            # all online users have a description that starts with Playing or
            # Joinable
            if gDesc.startswith("Playing") or gDesc.startswith("Joinable"):
                gPres = "Online"
            
            # save the gamer picture if it is not already cached
            gPic = self.saveGamerPicture(gPicURL)
            
            if gTag in self.liveFriends:
                # record the old status since the friend is already in the dict
                self.liveFriends[gTag].update(gTag, gPic, gPicURL, gPres, \
                    gDesc)
            else:
                self.liveFriends[gTag] = \
                    LiveFriend(gTag, gPic, gPicURL, gPres, gDesc)
    
            i = i+1

        return

    def disconnect(self):
        # This is typically used when 'disconnecting' from the Live site in the
        # controlling program.
        
        # clear the friends list
        del self.liveFriends
        self.liveFriends = {}
        
        return
