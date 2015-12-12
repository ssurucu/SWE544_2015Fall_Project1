import sys
import socket
import threading
import Queue
from PyQt4 import QtCore, QtGui
from client_UI import Ui_MainWindow
import time

screenQueue = Queue.Queue()
threadQueue = Queue.Queue()
onlineMemberQueue = Queue.Queue()
s = socket.socket()
host = ""
port = ""


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

        # timer has been set for updating channel window every 10ms
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateChannelWindow)
        self.timer.start(10)

        # timer has been set for updating member list every 1.5s
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.memberListRefresh)
        self.timer2.start(1500)

        # timer has been set for getting member list every 1.5s
        self.timer3 = QtCore.QTimer()
        self.timer3.timeout.connect(self.memberListGet)
        self.timer3.start(1500)

        readerThread = ReadQThread()
        readerThread.data_read.connect(self.updateChannelWindow)
        self.threads.append(readerThread)
        readerThread.start()

        writerThread = WriteQThread()
        writerThread.data_read.connect(self.updateChannelWindow)
        self.threads.append(writerThread)
        writerThread.start()

    # this function controls of the availability of the sendMessage button
    def statusSendButton(self):
        if self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(True)
        if not self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(False)

    # this function send text from messageTextLine to outgoing_parser
    def sendMessage(self):
        self.outgoing_parser(self.ui.messageTextLine.text())
        self.ui.messageTextLine.setText("")

    # this function parses the message texts into the format of protocol
    def outgoing_parser(self, data):
        if data[0] == "/":
            if data[1:4] == "msg":
                rest = str(data[5:]).partition(' ')
                threadQueue.put(str(("MSG ") + rest[0] + ":" + rest[2]))
                screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " " + data)
            elif data[1:5] == "nick":
                rest = data[6:]
                threadQueue.put(str(("USR ") + str(rest)))
                screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " " + data)
            elif data[1:5] == "quit":
                threadQueue.put(str("QUI"))
            else:
                screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " -Local-: " + data)
                screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " -Local-: Command error")
        else:
            threadQueue.put(str("SAY " + data))
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " -Local-: " + data)

    # a shortcut for sending private message, when click on a user from online users list, it will put the needed command in the textbox
    def item_click(self, item):
        self.ui.messageTextLine.setText("/msg " + item.text() + " ")

    # this function gets item(s) from screenqueue (if any exits) and adds to messageScreen
    def updateChannelWindow(self):
        if screenQueue.qsize() > 0:
            queue_message = screenQueue.get()
            self.ui.listWidget.addItem(unicode(queue_message))
            self.ui.listWidget.scrollToBottom()

    # sends LSQ command frequently to get the online users list
    def memberListGet(self):
        threadQueue.put('LSQ')

    def memberListRefresh(self):
        self.ui.onlineMembersCountLabel.setText(str(self.ui.onlineMembersList.count()))
        self.ui.onlineMembersList.clear()
        while onlineMemberQueue.qsize() > 0:
            onlineUser = onlineMemberQueue.get()
            self.ui.onlineMembersList.addItem(unicode(onlineUser))
        self.ui.onlineMembersCountLabel.setText(str(self.ui.onlineMembersList.count()))

    def connectToIRCServer(self):
        self.ui.listWidget.addItem('Please be patient while your connection is established with the server...')

        # host = socket.gethostname()
        # port = 55778
        # host = '178.233.19.205'
        # port = 12345

        s.connect((host, int(port)))

        self.ui.listWidget.addItem('Now you are connected to the server! Feel free to chat')
        self.ui.listWidget.addItem('Send message as /nick {nickname} to see who are online! ')
        self.ui.listWidget.addItem('---------------------------------------------------')

class ReadQThread(QtCore.QThread):
    data_read = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            data = s.recv(1024)
            self.incoming_parser(data)

    def incoming_parser(self, data):
        print data;
        if data[0:3] == "TIC":
            # threadQueue.put("TOC")
            s.send("TOC");
            print ''
        if data[0:3] == "HEL":
            screenQueue.put(
                time.strftime("[%H:%M:%S]", time.gmtime()) + " -Server-: Welcome aboard!Registered as <" + data[
                                                                                                           4:] + ">")
        if data[0:3] == "REJ":
            screenQueue.put(time.strftime("[%H:%M:%S]",
                                          time.gmtime()) + " -Server-: There is already a user, choose another nickname")
        if data[0:3] == "BYE":
            sys.exit(app.exec_())
        if data[0:3] == "LSA":
            onlineMemberList = data[4:].split(':')
            for x in onlineMemberList:
                onlineMemberQueue.put(str(x))
        if data[0:3] == "TOC":
            print ''
        if data[0:3] == "SAY":
            text = data[4:].split(':')
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " <" + str(text[0]) + ">: " + str(text[1]))
        if data[0:6] == "TICSAY":
            text = data[7:].split(':')
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " <" + str(text[0]) + ">: " + str(text[1]))
        if data[0:3] == "MNO":
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + "No user found for the private message")
        if data[0:3] == "MSG":
            text = data[4:].split(':')
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " *" + str(text[0]) + "*: " + str(text[1]))
        if data[0:3] == "ERR":
             print 'Command Error'
        if data[0:3] == "ERL":
             print 'No command has been entered'
        if data[0:3] == "SYS":
            print "S_" + (data)
            screenQueue.put(time.strftime("[%H:%M:%S]", time.gmtime()) + " -Server-: " + data[4:])


class WriteQThread(QtCore.QThread):
    data_read = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            if threadQueue.qsize() > 0:
                queue_message = threadQueue.get()
                try:
                    s.send(queue_message)
                except socket.error:
                    s.close()
                    break


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    host = raw_input("Please enter hostname: ")
    port = raw_input("Please enter port: ")
    myapp = ClientDialog()
    # myapp.show()
    sys.exit(app.exec_())
