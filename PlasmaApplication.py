from Foundation import *
from AppKit import *
from PlasmaWindowController import *
from WebKit import *

class PlasmaApplication(NSApplication):
  """
  Main application class
  """
  controllers = []
  windows = []
  def finishLaunching(self):
    super(PlasmaApplication, self).finishLaunching()
    self.setPresentationOptions_(NSApplicationPresentationAutoHideMenuBar | NSApplicationPresentationAutoHideDock)
    screens = NSScreen.screens()
    NSMenu.setMenuBarVisible_(False)
    for screen in screens:
        window = NSWindow.alloc()
        rect = Foundation.NSMakeRect(0,0,0,0)
        window.initWithContentRect_styleMask_backing_defer_(rect, NSBorderlessWindowMask, NSBackingStoreBuffered, False)
        window.setFrame_display_animate_(screen.frame(), YES, YES)
        window.makeKeyAndOrderFront_(None)
        controller = PlasmaWindowController.alloc().initWithWindow_(window)
        self.windows.append(window)
        self.controllers.append(controller)
