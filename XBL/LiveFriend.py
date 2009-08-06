#!/usr/bin/python

# LiveFriend -- a class to hold Xbox Live friends
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

class LiveFriend:

    def __init__(self, gTag, gPic, gPicURL, gPres, gDesc):
        self.gamerTag = gTag
        self.gamerPic = gPic
        self.gamerPicURL = gPicURL
        self.status = gPres
        self.oldStatus = None
        self.description = gDesc
        self.descUpdated = False

    def update(self, gTag, gPic, gPicURL, gPres, gDesc):
        self.setOldStatus()
        self.setDescUpdated(gDesc)
        self.gamerTag = gTag
        self.gamerPic = gPic
        self.gamerPicURL = gPicURL
        self.status = gPres
        self.description = gDesc

    def setOldStatus(self):
        self.oldStatus = self.status        

    def setDescUpdated(self, gDesc):
        if gDesc != self.description:
            self.descUpdated = True
        else:
            self.descUpdated = False

    def isOnline(self):
        """ Return True if the friend status is 'Online' """
        if self.status == "Online":
            return True
        return False
    
    def isAway(self):
        """ Return True if the friend status is 'Away' """
        if self.status == "Away":
            return True
        return False
    
    def isBusy(self):
        """ Return True if the friend status is 'Busy' """
        if self.status == "Busy":
            return True
        return False

    def isPending(self):
        """ Return True if the friend status is 'Pending' """
        if self.status == "Pending":
            return True
        return False
    
    def isOffline(self):
        """ Return True if the friend status is 'Offline' """
        if self.status == "Offline":
            return True
        return False

