# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homelayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(1031, 852)
        self.verticalLayoutWidget = QtWidgets.QWidget(Home)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(150, 30, 721, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Home)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(440, 460, 160, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_begin = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_begin.setFont(font)
        self.btn_begin.setObjectName("btn_begin")
        self.verticalLayout_2.addWidget(self.btn_begin)
        self.btn_show_readme = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_show_readme.setFont(font)
        self.btn_show_readme.setObjectName("btn_show_readme")
        self.verticalLayout_2.addWidget(self.btn_show_readme)
        self.label_2 = QtWidgets.QLabel(Home)
        self.label_2.setGeometry(QtCore.QRect(900, 800, 111, 20))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Home"))
        self.label.setText(_translate("Home", "English, Sinhala & Tamil Sentence Alignment"))
        self.btn_begin.setText(_translate("Home", "Begin"))
        self.btn_show_readme.setText(_translate("Home", "ReadMe"))
        self.label_2.setText(_translate("Home", "Team Cerebrex"))

