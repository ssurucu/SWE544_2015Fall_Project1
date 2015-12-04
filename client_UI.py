# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_UI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(782, 542)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.sendMessageButton = QtGui.QPushButton(self.centralwidget)
        self.sendMessageButton.setGeometry(QtCore.QRect(390, 440, 101, 31))
        self.sendMessageButton.setObjectName(_fromUtf8("sendMessageButton"))
        self.onlineMembersLabel = QtGui.QLabel(self.centralwidget)
        self.onlineMembersLabel.setGeometry(QtCore.QRect(510, 10, 101, 16))
        self.onlineMembersLabel.setObjectName(_fromUtf8("onlineMembersLabel"))
        self.onlineMembersCountLabel = QtGui.QLabel(self.centralwidget)
        self.onlineMembersCountLabel.setGeometry(QtCore.QRect(610, 10, 101, 16))
        self.onlineMembersCountLabel.setObjectName(_fromUtf8("onlineMembersCountLabel"))
        self.onlineMembersList = QtGui.QListWidget(self.centralwidget)
        self.onlineMembersList.setGeometry(QtCore.QRect(510, 30, 231, 461))
        self.onlineMembersList.setObjectName(_fromUtf8("onlineMembersList"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 481, 401))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.onlineMembersLabel_2 = QtGui.QLabel(self.centralwidget)
        self.onlineMembersLabel_2.setGeometry(QtCore.QRect(10, 480, 221, 16))
        self.onlineMembersLabel_2.setObjectName(_fromUtf8("onlineMembersLabel_2"))
        self.messageTextLine = QtGui.QLineEdit(self.centralwidget)
        self.messageTextLine.setGeometry(QtCore.QRect(10, 440, 371, 31))
        self.messageTextLine.setObjectName(_fromUtf8("messageTextLine"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SC2015_IRCClient", None))
        self.sendMessageButton.setText(_translate("MainWindow", "Send", None))
        self.onlineMembersLabel.setText(_translate("MainWindow", "Online Members", None))
        self.onlineMembersCountLabel.setText(_translate("MainWindow", "0", None))
        self.onlineMembersLabel_2.setText(_translate("MainWindow", "(Tip: Press \"Enter\" to send message)", None))

