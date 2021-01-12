import sys
import random
import worker
from os.path import expanduser
from kishky.DocAlignment import runDatewise
from layouts.mainlayout import Ui_SentenceAlignment as UiForm_main
from layouts.homelayout import Ui_Home as UiForm_home
from layouts.readmelayout import Ui_ReadMe as UiForm_readme
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from kishky.CreateEmbeddings import createEmbeddings
from sentenceAlignment.align import alignSentences
from pyqtspinner import spinner

class HomeWidget(QtWidgets.QMainWindow, UiForm_home):

    def __init__(self,parent=None):
        super(HomeWidget,self).__init__(parent)
        self.setupUi(self)
        self.btn_show_readme.clicked.connect(self.showReadMe)
        self.btn_begin.clicked.connect(self.openSentenceAlignment)


    def showReadMe(self):
        self.readme = ReadMeWidget()

    def openSentenceAlignment(self):
        self.mainwidget = MainWidget()
        self.mainwidget.show()
        self.hide()

class ReadMeWidget(QtWidgets.QMainWindow, UiForm_readme):

    def __init__(self,parent=None):
        super(ReadMeWidget,self).__init__(parent)
        self.setupUi(self)
        self.btn_close.clicked.connect(self.closeWindow)
        self.show()
    
    def closeWindow(self):
        self.close()

class MainWidget(QtWidgets.QMainWindow, UiForm_main):

    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.setSourceEmbedding)
        self.pushButton_2.clicked.connect(self.setTargetEmbedding)
        self.pushButton_3.clicked.connect(self.setTargetText)
        self.pushButton_4.clicked.connect(self.setSourceText)
        self.pushButton_5.clicked.connect(self.docalign)
        self.pushButton_6.clicked.connect(self.testTable)
        self.btn_back.clicked.connect(self.goBack)
        self.checkBox_createEmbeddings.clicked.connect(self.changeEmbeddingOptionsVisibility)
        self.comboBox_sourceLang.addItems(["En", "Si", "Ta"])
        self.comboBox_targetLang.addItems(["En", "Si", "Ta"])

    def changeEmbeddingOptionsVisibility(self):
        if (self.checkBox_createEmbeddings.isChecked()):
            # self.pushButton.setDisabled(True)
            # self.pushButton_2.setDisabled(True)
            self.comboBox_sourceLang.setDisabled(False)
            self.comboBox_targetLang.setDisabled(False)
            self.label_9.setDisabled(False)
            self.label_10.setDisabled(False)
        else:
            self.comboBox_sourceLang.setDisabled(True)
            self.comboBox_targetLang.setDisabled(True)
            self.label_9.setDisabled(True)
            self.label_10.setDisabled(True)
            # self.pushButton.setDisabled(False)
            # self.pushButton_2.setDisabled(False)

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
        # print("Starting Document Alignment")
        # print("A - "+self.sourceText)
        # print("B - "+self.targetText)

        if (self.checkBox_createEmbeddings.isChecked()):
            self.setEmbeddings()

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

            self.thread = QtCore.QThread(self)
            self.worker = worker.Worker()
            self.worker.sourceEmbedding = self.sourceEmbedding
            self.worker.targetEmbedding = self.targetEmbedding
            self.worker.sourceText = self.sourceText
            self.worker.targetText = self.targetText
            self.worker.distance_metric = distance_metric
            self.worker.moveToThread(self.thread) # worker will be runned in another thread
            self.worker.done.connect(self.onThreadDone) # Call load_data_to_tree when worker.done is emitted
            self.thread.started.connect(self.worker.doWork) # Call worker.doWork when the thread starts
            self.thread.start() # Start the thread (and run doWork)
            self.waiting_spinner = spinner.WaitingSpinner(self, disableParentWhenSpinning=True, line_width=5, line_length=30, radius=30)
            self.waiting_spinner.start()
        else:
            print("Please select at least one distance measurement")

    def onThreadDone(self, aligned_sentences):
        for i in aligned_sentences:
            self.waiting_spinner.stop()
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            numcols = self.tableWidget.columnCount()
            numrows = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(numrows)
            self.tableWidget.setColumnCount(numcols)
            self.tableWidget.setItem(numrows - 1, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.tableWidget.setItem(numrows - 1, 1, QtWidgets.QTableWidgetItem(i[1]))

    def testTable(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        numcols = self.tableWidget.columnCount()
        numrows = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(numrows)
        self.tableWidget.setColumnCount(numcols)
        self.tableWidget.setItem(numrows - 1, 0, QtWidgets.QTableWidgetItem("Test"))
        self.tableWidget.setItem(numrows - 1, 1, QtWidgets.QTableWidgetItem("Test"))

    def setEmbeddings(self):
        src_txt_input_path = self.sourceText
        src_txt_output_path = self.sourceEmbedding
        target_txt_input_path = self.targetText
        target_txt_output_path = self.targetEmbedding
        createEmbeddings(src_txt_input_path, src_txt_output_path, str(self.comboBox_sourceLang.currentText()).lower())
        createEmbeddings(target_txt_input_path, target_txt_output_path, str(self.comboBox_targetLang.currentText()).lower())
    
    def goBack(self):
        self.home = HomeWidget()
        self.home.show()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    home = HomeWidget()
    home.show()

    sys.exit(app.exec_())