from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys

class MiniWrapper(QObject):
    def __init__(self, parent=None):
        super(MiniWrapper, self).__init__(parent)

    @pyqtSlot(str, str)
    def onJSEvent(self, name, msg):
        print "Form (\"%s\"): Value (\"%s\")" % (name, msg)


class InspectForms(QApplication):


    def __init__(self, argv):
        super(QApplication, self).__init__(argv)
        self.mini = MiniWrapper()
        self.browser = QWebView()
        self.browser.show()
        self.browser.resize(800, 600)
        self.browser.load(QUrl(argv[1]))
        self.page = self.browser.page()

        self.page.loadFinished.connect(self.injectJavaScript)

    def injectJavaScript(self, **kwargs):
        frame = self.page.mainFrame()
        frame.addToJavaScriptWindowObject("injectedObject", self.mini)
        forms = frame.findAllElements("form")
        for form in forms:
            inputs = form.findAll("input")
            for input_ in inputs:
                input_.setAttribute("onchange", QString("injectedObject.onJSEvent(this.name, this.value);"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s URL" % sys.argv[0]
        sys.exit(1)
    try:
        app = InspectForms(sys.argv)
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        app.quit()
