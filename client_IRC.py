import sys
import socket

from PyQt4 import QtCore, QtGui
from client_UI import Ui_MainWindow

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.onlineMembersList.itemClicked.connect(self.item_click)
        self.ui.sendMessageButton.clicked.connect(self.sendMessage)

        self.ui.listWidget.addItem('Welcome to SC2015_IRCClient!')


        self.connectToIRCServer();
        self.memberListRefresh();
        self.ui.messageTextLine.returnPressed.connect(self.sendMessage)
        self.ui.messageTextLine.setPlaceholderText('Please enter your message')
        self.ui.sendMessageButton.setEnabled(False)
        self.ui.messageTextLine.textChanged.connect(self.statusSendButton)


    def statusSendButton(self):
        if self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(True)
        if not self.ui.messageTextLine.text():
            self.ui.sendMessageButton.setEnabled(False)


    def sendMessage(self):
        if self.ui.messageTextLine.text():
            self.ui.listWidget.addItem(self.ui.messageTextLine.text())
            self.ui.messageTextLine.setText("")

    def item_click(self, item):
        print item

    def memberListRefresh(self):
        for x in range(0, 3):
            self.ui.onlineMembersList.addItem(str(x) + "_Sinan Can")
        self.ui.onlineMembersCountLabel.setText(str(self.ui.onlineMembersList.count()))


    def connectToIRCServer(self):
        self.ui.listWidget.addItem('Please be patient while your connection is established with the server...')
        s = socket.socket()
        host = socket.gethostname()
        port = 55778

        s.connect((host, port))

        self.ui.listWidget.addItem(s.recv(1024))
        self.ui.listWidget.addItem('---------------------------------------------------')

        print s.recv(1024)
        s.close



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
