from PyQt5.QtCore import QObject, pyqtSignal
from kishky.DocAlignment import runDatewise
from sentenceAlignment.align import alignSentences

class Worker(QObject):

    done = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sourceEmbedding = ""
        self.targetEmbedding = ""
        self.sourceText = ""
        self.targetText = ""
        self.distance_metric = ""

    def doWork(self):
        aligned = runDatewise(self.sourceEmbedding,self.targetEmbedding,self.sourceText,self.targetText, self.distance_metric)
        aligned_sentences = alignSentences(aligned, self.distance_metric)
        self.done.emit(aligned_sentences)
