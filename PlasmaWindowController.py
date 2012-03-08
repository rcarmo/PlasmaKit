from Foundation import *
from AppKit import *
from ScriptingBridge import *
import WebKit

from Carbon.AppleEvents import kAEISGetURL, kAEInternetSuite
import struct
import objc
import re
import traceback
import os
from time import time as epoch_time
import commands

class PlasmaWindowController (NSWindowController):
    def initWithWindow_(self, window):
        super(PlasmaWindowController, self).initWithWindow_(window)
        frame = window.screen().frame()
        self.width = frame.size.width
        self.height = frame.size.height
        print self.width, self.height
        NSCursor.setHiddenUntilMouseMoves_(YES)
        self.webView = WebKit.WebView.alloc()
        self.webView.initWithFrame_(frame)
        self.resourcePath = NSBundle.mainBundle().resourcePath()
        self.baseURL = NSURL.alloc().initFileURLWithPath_(NSString.stringWithString_(self.resourcePath))
        print "Awake. Webview ready but unbound.", self.resourcePath
        self.performSelector_withObject_afterDelay_('showStatus', None, 0)
    
    def showStatus(self):
        path = self.resourcePath
        display = int(window.screen())
        interfaces = map(lambda x: (x.split(":",1)[0], x.split(" ")[1:]),filter(lambda x: "en0:" in x or "en1:" in x, commands.getoutput("ifconfig").replace("\n\t",' ').replace("  "," ").replace("="," ").split("\n")))
        self.webView.mainFrame().loadHTMLString_baseURL_(open(os.path.join(self.resourcePath,'status.html'),'r').read()  % locals(), self.baseURL)
        self.window().setContentView_(self.webView)
        self.webView.mainFrame().frameView().setAllowsScrolling_(False)
        
    def applicationDidFinishLaunching_(self, sender):
        print "DidFinishLaunching"
        return
  
    def applicationWillTerminate_(self, sender):
        # kill the poller and any other long-running things
        NSObject.cancelPreviousPerformRequestsWithTarget_( self )
  
    def applicationWillResignActive_(self, notification):
        self.css = "inactive.css"
        self.webView.windowScriptObject().evaluateWebScript_("document.getElementById('mode').href = '%s'" % self.css)
  
    def applicationWillBecomeActive_(self, notification):
        self.css = "active.css"
        self.webView.windowScriptObject().evaluateWebScript_("document.getElementById('mode').href = '%s'" % self.css)

    def setScreen(self, screen):
        self.screen = screen

    def poll(self):
        print_info( "\n---- poll start ----" )    
        # First thing I do, schedule the next poll event, so that I can just return with impunity from this function
        if not NSUserDefaults.standardUserDefaults().boolForKey_("useHotkey"):
            self.performSelector_withObject_afterDelay_( 'poll', None, 2 )

    def updateInfo(self):
        base = NSURL.fileURLWithPath_( NSBundle.mainBundle().resourcePath() )
        self.setWebContent_( clue.content() ) # will initially be 'thinking...'
    
        # always safe
        self.window().setHidesOnDeactivate_( False )
    
        if NSUserDefaults.standardUserDefaults().boolForKey_("bringAppForward"):
            # slightly voodoo, this. But otherwise it doesn't seem 100% reliable
            self.showWindow_(self)
            self.window().orderFrontRegardless()

        if NSUserDefaults.standardUserDefaults().boolForKey_("alwaysOnTop"):
            self.window().setLevel_( NSFloatingWindowLevel ) # 'on top'

        self.window().display()
    
    def setWebContent_(self, html):
        """ the base path of the webview is the resource folder, so I can use relative paths to refer to the CSS. """
        base = NSURL.fileURLWithPath_( NSBundle.mainBundle().resourcePath() )
        self.webView.mainFrame().loadHTMLString_baseURL_("""
          <html>
          <head>
          <link rel="stylesheet" href="%s" type="text/css" id="mode"/>                
          <link rel="stylesheet" href="%s" type="text/css" id="generic"/>                
          </head>
          <body>
          %s
          <body>
          </html>
          """ % (self.css,"style.css",html), base)
