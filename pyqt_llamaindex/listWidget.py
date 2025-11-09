import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QPushButton, \
    QSizePolicy, QFileDialog, QFrame


class FileListWidget(QWidget):
    itemUpdate = pyqtSignal(bool)
    onDirectorySelected = pyqtSignal()
    clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__dirLblPrefix = 'Directory: '
        self.__curDirName = ''

    def __initUi(self):
        lbl = QLabel('Files')
        setDirBtn = QPushButton('Set Directory')
        setDirBtn.clicked.connect(self.__setDir)
        self.__dirLbl = QLabel(self.__dirLblPrefix)

        lay = QHBoxLayout()
        lay.addWidget(lbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.MinimumExpanding))
        lay.addWidget(setDirBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__listWidget = QListWidget()
        self.__listWidget.itemClicked.connect(self.__sendDir)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(sep)
        lay.addWidget(self.__dirLbl)
        lay.addWidget(self.__listWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

    def __setDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        ext_lst = ['.txt']
        if directory:
            self.__listWidget.clear()
            filenames = list(filter(lambda x: os.path.splitext(x)[-1] in ext_lst, os.listdir(directory)))
            self.__listWidget.addItems(filenames)
            self.itemUpdate.emit(len(filenames) > 0)
            self.__curDirName = directory
            self.__dirLbl.setText(self.__curDirName.split('/')[-1])

            self.__listWidget.setCurrentRow(0)
            # activate event as clicking first item (because this selects the first item anyway)
            item = self.__listWidget.currentItem()
            if item:
                self.clicked.emit(os.path.join(self.__curDirName, item.text()))
            self.onDirectorySelected.emit()

    def getDir(self):
        return self.__curDirName

    def __sendDir(self, item):
        self.clicked.emit(os.path.join(self.__curDirName, item.text()))