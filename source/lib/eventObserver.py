from vanilla import *
from AppKit import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver
import fnmatch

class NotificationItem(object):

    def __init__(self, notification):
        self.notification = notification

    def __repr__(self):
        return self.notification["notificationName"]

keyAttributes = {NSFontAttributeName : NSFont.fontWithName_size_("Menlo-Bold", 15)}
valueAttributes = {NSFontAttributeName : NSFont.fontWithName_size_("Menlo-Bold", 10), NSForegroundColorAttributeName : NSColor.darkGrayColor()}

class Observer(BaseWindowController):

    def __init__(self):

        self.w = FloatingWindow((400, 400), "mojo.event observer", minSize=(200, 200))
        self.w.list = List((10, 10, 200, -40), [], selectionCallback=self.listSelection)
        self.w.info = TextEditor((220, 10, -10, -40), readOnly=True)
        self.w.ignoreText = TextBox((10, -30, 100, 22), "Ignore:")
        self.w.ignore = EditText((70, -30, -100, 22), "mouseMoved")
        self.w.clear = Button((-70, -30, 60, 22), "Clear", self.clearListCallback)

        addObserver(self, "notification", None)
        self.setUpBaseWindowBehavior()
        self.w.open()

    def windowCloseCallback(self, sender):
        removeObserver(self, None)
        super(Observer, self).windowCloseCallback(sender)

    def listSelection(self, sender):
        sel = sender.getSelection()
        for i in sel:
            item = sender[i]
            notification = item.notification
            keys = sorted(notification.keys())
            txt = NSMutableAttributedString.alloc().init()
            for key in keys:
                attributedString = NSMutableAttributedString.alloc().initWithString_attributes_(key, keyAttributes)
                txt.appendAttributedString_(attributedString)
                value = "\n%s\n\n" % str(notification[key])
                attributedString = NSMutableAttributedString.alloc().initWithString_attributes_(value, valueAttributes)
                txt.appendAttributedString_(attributedString)
            self.w.info.getNSTextView().textStorage().setAttributedString_(txt)

    def clearListCallback(self, sender):
        self.w.list.set([])
        self.w.info.set("")

    def checkCanIgnore(self, notification, toIgnore):
        for item in toIgnore:
            if notification == item or fnmatch.fnmatch(notification, item):
                return True
        return False

    def notification(self, notification):
        if self.checkCanIgnore(
            notification["notificationName"],
            self.w.ignore.get().split(" ")
            ):
            return
        self.w.list.append(NotificationItem(notification))
        self.w.list.getNSTableView().scrollRowToVisible_(len(self.w.list) - 1)

Observer()
