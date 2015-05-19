from AppKit import NSObject, NSThread

import os

settingsIdentifier = "com.typemytype.toolbox"


class Report(object):

    def __init__(self):
        self._data = []

    def write(self, value):
        self._data.append(value)

    def writeTitle(self, value, underline="-"):
        self.write(value)
        self.write(underline * len(value))

    def newLine(self):
        self._data.append("")

    def writeDict(self, d):
        maxLength = 0
        for key in d:
            l = len(key)
            if l > maxLength:
                maxLength = l

        for key in sorted(d):
            value = d[key]
            t = "%s = %s" % (key.ljust(maxLength), value)
            self.write(t)

    def writeList(self, l):
        for i in l:
            self.write(str(i))

    def save(self, path):
        f = file(path, "w")
        f.write("\n".join(self._data))
        f.close()


def updateWithDefaultValues(data, defaults):
    for key, value in defaults.items():
        if key in data:
            continue
        data[key] = value


def buildTree(path):
    if not os.path.exists(path):
        os.makedirs(path)


class TaskRunner(NSObject):

    def __new__(cls, *args, **kwargs):
        return cls.alloc().init()

    def __init__(self, callback, threaded, progress, kwargs=dict()):
        self._callback = callback
        self._kwargs = kwargs
        self._progress = progress

        if threaded:
            self._thread = NSThread.alloc().initWithTarget_selector_object_(self, "runTask:", None)
            self._thread.start()
        else:
            self.runTask_(None)

    def runTask_(self, sender):
        try:
            self._callback(progress=self._progress, **self._kwargs)
        except:
            import traceback
            errorMessage = [
                    "*"*30,
                    traceback.format_exc(5),
                    "*"*30
                    ]
            print "\n".join(errorMessage)
        self._progress.close()