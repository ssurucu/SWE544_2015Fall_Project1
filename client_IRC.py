import sys
import socket
import threading
import Queue
from PyQt4 import QtCore, QtGui
from client_UI import Ui_MainWindow
import time

screenQueue = Queue.Queue()
threadQueue = Queue.Queue()
s = socket.socket()


class ClientDialog(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.onlineMembersList.itemClicked.connect(self.item_click)
        self.ui.sendMessageButton.clicked.connect(self.sendMessage)

        self.ui.listWidget.addItem('Welcome to SC2015_IRCClient!')

        print threading.current_thread()
        self.show()
        self.connectToIRCServer();
        self.memberListRefresh();
        self.ui.messageTextLine.returnPressed.connect(self.sendMessage)
        self.ui.messageTextLine.setPlaceholderText('Please enter your message')
        self.ui.sendMessageButton.setEnabled(False)
        self.ui.messageTextLine.textChanged.connect(self.statusSendButton)

        self.threads = []


        readerThread = ReadQThread()
        readerThread.data_downloaded.connect(self.updateChannelWindow)
        self.threads.append(readerThread)
        readerThread.start()

        writerThread = WriteQThread()
        writerThread.data_downloaded.connect(self.updateChannelWindow)
        self.threads.append(writerThread)
        writerThread.start()

    def statusSendButton(self):
        if self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(True)
        if not self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(False)

    # this function adds message text to the screenqueue
    def sendMessage(self):
        if self.ui.messageTextLine.text():
            # to add to the messageScreen
            screenQueue.put("-Local-: " + self.ui.messageTextLine.text())
            # to send to the server
            threadQueue.put(self.ui.messageTextLine.text())
            self.ui.messageTextLine.setText("")

    def item_click(self, item):
        print item

    # this function gets item(s) from screenqueue (if any exits) and adds to messageScreen
    def updateChannelWindow(self):
        if screenQueue.qsize() > 0:
            queue_message = screenQueue.get()
            self.ui.listWidget.addItem(unicode(queue_message))
            self.ui.listWidget.scrollToBottom()

    def memberListRefresh(self):
        for x in range(0, 3):
            self.ui.onlineMembersList.addItem(str(x) + "_Sinan Can")
        self.ui.onlineMembersCountLabel.setText(str(self.ui.onlineMembersList.count()))

    def connectToIRCServer(self):
        self.ui.listWidget.addItem('Please be patient while your connection is established with the server...')

        # host = socket.gethostname()
        # port = 55778
        host = '178.233.19.205'
        port = 12345

        s.connect((host, port))

        self.ui.listWidget.addItem('Now you are connected to the server! Feel free to chat')
        self.ui.listWidget.addItem('---------------------------------------------------')

        # _WriteThread = threading.Thread(target=WriteThread, args={"WriteThread", s, sendQueue})
        # _WriteThread.start()
        # _WriteThread.join()

        # _ReadThread = threading.Thread(target=ReadThread, args={self, "ReadThread", s, sendQueue, screenQueue})
        # _ReadThread.start()
        # _ReadThread.join()

        print s.recv(1024)
        s.close


class ReadQThread(QtCore.QThread):
    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            data = s.recv(1024)
            if data != "":
                screenQueue.put("-Server-: " + unicode(data))
                self.data_downloaded.emit('%s' % (data))


class WriteQThread(QtCore.QThread):
    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            if threadQueue.qsize() > 0:
                queue_message = threadQueue.get()
                try:
                    print queue_message
                    s.send(queue_message)
                except socket.error:
                    s.close()
                    break


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = ClientDialog()
    #myapp.show()
    sys.exit(app.exec_())
