import sys
import random
from os.path import expanduser
from kishky.DocAlignment import runDatewise
from layout import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

class MyWidget(QtWidgets.QMainWindow,Ui_Form):

    def __init__(self,parent=None):
        super(MyWidget,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.setSourceEmbedding)
        self.pushButton_2.clicked.connect(self.setTargetEmbedding)
        self.pushButton_3.clicked.connect(self.setTargetText)
        self.pushButton_4.clicked.connect(self.setSourceText)
        self.pushButton_5.clicked.connect(self.docalign)
        self.pushButton_6.clicked.connect(self.testTable)
        self.checkBox_createEmbeddings.clicked.connect(self.changeEmbeddingPathVisibility)

    def changeEmbeddingPathVisibility(self):
        if (self.checkBox_createEmbeddings.isChecked()):
            self.pushButton.setDisabled(True)
            self.pushButton_2.setDisabled(True)
        else:
            self.pushButton.setDisabled(False)
            self.pushButton_2.setDisabled(False)

    def setSourceEmbedding(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self,'Select Source Embedding Directory')
        if filename:
            self.sourceEmbedding = filename+'/'
            self.label_3.setText(filename)

    def setTargetEmbedding(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Target Embedding Directory')
        if filename:
            self.targetEmbedding = filename+'/'
            self.label_4.setText(filename)

    def setSourceText(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Source Text Directory')
        if filename:
            self.sourceText = filename+'/'
            self.label_8.setText(filename)

    def setTargetText(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Target Text Directory')
        if filename:
            self.targetText = filename+'/'
            self.label_6.setText(filename)

    def docalign(self):
        print("Starting Document Alignment")
        print("A - "+self.sourceText)
        print("B - "+self.targetText)

        if (self.checkBox_createEmbeddings.isChecked()):
            self.createEmbeddings()

        if (self.checkBox_cosine.isChecked() or self.checkBox_metric.isChecked() or self.checkBox_euclidean.isChecked()):
            distance_metric = 0

            if (self.checkBox_cosine.isChecked() and self.checkBox_metric.isChecked() and self.checkBox_euclidean.isChecked()):
                distance_metric = 1
                print("all")
            elif (self.checkBox_cosine.isChecked() and self.checkBox_metric.isChecked()):
                print("metric + cosine")
                distance_metric = 2
            elif (self.checkBox_cosine.isChecked() and self.checkBox_euclidean.isChecked()):
                print("cosine + euc")
                distance_metric = 3
            elif (self.checkBox_metric.isChecked() and self.checkBox_euclidean.isChecked()):
                print("metric + euc")
                distance_metric = 4
            elif (self.checkBox_metric.isChecked()):
                print("metric")
                distance_metric = 5
            elif (self.checkBox_euclidean.isChecked()):
                print("euc")
                distance_metric = 6
            else:
                print("cosine")
                distance_metric = 7
            aligned = runDatewise(self.sourceEmbedding,self.targetEmbedding,self.sourceText,self.targetText, distance_metric)

            for i in aligned:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                numcols = self.tableWidget.columnCount()
                numrows = self.tableWidget.rowCount()
                self.tableWidget.setRowCount(numrows)
                self.tableWidget.setColumnCount(numcols)
                self.tableWidget.setItem(numrows - 1, 0, QtWidgets.QTableWidgetItem(i[0]))
                self.tableWidget.setItem(numrows - 1, 1, QtWidgets.QTableWidgetItem(i[1]))
            # here calls the doc align algorithm
        else:
            print("Please select at least one distance measurement")

    def testTable(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        numcols = self.tableWidget.columnCount()
        numrows = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)
        self.tableWidget.setItem(numrows - 1, 0, QtWidgets.QTableWidgetItem("Test"))
        self.tableWidget.setItem(numrows - 1, 1, QtWidgets.QTableWidgetItem("Test"))

    def createEmbeddings(self):
        self.sourceEmbedding = "C:/Users/Dilan Sachintha/Desktop/embeddings/datewise/hiru/en/"
        self.targetEmbedding = "C:/Users/Dilan Sachintha/Desktop/embeddings/datewise/hiru/si/"
        self.label_3.setText(self.sourceEmbedding)
        self.label_4.setText(self.targetEmbedding)


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())


