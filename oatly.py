from cefpython3 import cefpython as cef

import bs4
import time
import platform
import sys
import os
import argparse
import random
from concurrent.futures import ThreadPoolExecutor

def set_javascript_bindings(browser):
    bindings = cef.JavascriptBindings(bindToFrames=False, bindToPopups=False)
    #  bindings.SetFunction("html_to_data_uri", html_to_data_uri)
    browser.SetJavascriptBindings(bindings)


def set_client_handlers(browser):
    client_handlers = [LoadHandler()]
    for handler in client_handlers:
        browser.SetClientHandler(handler)


def speakNotification():
    os.system('say "Slots for delivery opened"')



def macOS_notify(title, text, sound):
    os.system("""osascript -e 'display notification "%s" with title "%s" sound name "%s"' """ %(text, title, sound))


class TimeSlotVisitor(object):

    def Visit(self, value):
        if value.count('Oatly, Oat Milk') > 0:
            print('Grab your oatly!')
            for notification in notifications:
                notification()
            try:
                macOS_notify("Oatly", "Oatly", "default")
            except:
                pass
        else:
            print('God! Why are you doing this to me')

        browser.Reload()

def refresh_without_freezing(v, browser):
    time.sleep(v)
    browser.GetMainFrame().GetSource(timeslotvisitor)


class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        # This callback is called twice, once when loading starts
        # (is_loading=True) and second time when loading ends
        # (is_loading=False).
        if not is_loading:
            url = browser.GetUrl()

            print("At url: {}".format(url))

            if FRONT_URL in url:
                print("Store front page, Attempting to nav to Cart...")
                browser.LoadUrl("https://primenow.amazon.com/search?k=oatly")
            elif SEARCH_URL in url:
                v = parsed_args.sleep + random.random() * 5
                print ("Sleep for %fs, then reload" % v)
                pool.submit(refresh_without_freezing, v, browser)
                
            

def check_versions():
    ver = cef.GetVersion()
    print("[primenow.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[primenow.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[primenow.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[primenow.py] Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


import wx

class MyFrame(wx.Frame):
    def __init__(self):
        global browser

        settings = {
            "debug": False,
            "log_severity": cef.LOGSEVERITY_ERROR,
            "log_file": "debug.log"
        }

        browser = None


        check_versions()
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize(settings=settings)
        browser = cef.CreateBrowserSync(url="https://primenow.amazon.com/signin")
        browser.SetFocus(True)
        set_client_handlers(browser)
        set_javascript_bindings(browser)
        #  browser.ShowDevTools()
        cef.MessageLoop()
        self.browser = browser()

    def OnClose(self, event):
        self.browser.close()
        self.Destroy()
        cef.shutdown()

class MyApp(wx.App):
    def OnInit(self):
        frame = frame = MyFrame()
        self.SetTopWindow(frame)
        frame.show()
        return True

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--enable-say', action='store_true', help='Enable speech notiifcations')
parser.add_argument('--sleep', default=30, help='Amazon Username (optional for autocomplete)', type=int)
FRONT_URL = "https://primenow.amazon.com/storefront"
SEARCH_URL = "https://primenow.amazon.com/search"
parsed_args = parser.parse_args()


notifications = []
pool = ThreadPoolExecutor(max_workers=1)

timeslotvisitor = TimeSlotVisitor()


if parsed_args.enable_say:
    print("Speech support enabled.")
    notifications.append(speakNotification)

app = MyApp()
app.MainLoop()
# Important: do the wx cleanup before calling Shutdown
del app



# sth to do