#
#  main.py
#
#  Created by Rui Carmo on 2011-09-26
#  Published under the MIT license
#

#import modules required by application
import objc
import Foundation
import AppKit
import os
from AppKit import *
from PyObjCTools import AppHelper

# put external deps here where py2app can find them
import urllib, urllib2
import ScriptingBridge
import urlparse
import json
import WebKit

NSUserDefaults.standardUserDefaults().registerDefaults_({
    'bringAppForward':True,
    'firstRun':True,
    'debug':True
})

import PlasmaApplication
import PlasmaWindowController

# pass control to AppKit
AppHelper.runEventLoop()
