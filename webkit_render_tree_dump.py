from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys

class RenderTreeDump(QApplication):


    def __init__(self, argv):
        super(QApplication, self).__init__(argv)
        self.page = QWebPage()
        self.frame = self.page.mainFrame()
        self.frame.load(QUrl(argv[1]))
        self.page.loadFinished.connect(self.renderTreeDump)

    def renderTreeDump(self, **kwargs):
        print self.frame.renderTreeDump()
        sys.exit(self.quit())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s URL" % sys.argv[0]
        sys.exit(1)
    try:
        app = RenderTreeDump(sys.argv)
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit(app.quit())
