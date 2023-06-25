import os, sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

import openai
import requests
from PyQt5.QtCore import QCoreApplication, Qt, QSettings
from PyQt5.QtGui import QGuiApplication, QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, \
    QVBoxLayout, QSplitter, QSizePolicy, QFrame, QTextBrowser

from pyqt_llamaindex.chatWidget import ChatBrowser, Prompt
from pyqt_llamaindex.listWidget import FileListWidget
from pyqt_llamaindex.openAiThread import OpenAIThread
from pyqt_llamaindex.scripts import GPTLLamaIndexClass

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support
# qt version should be above 5.14
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

QApplication.setFont(QFont('Arial', 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # declare widgets in advance to prevent AttributeError
        self.__apiLineEdit = QLineEdit()
        self.__apiCheckPreviewLbl = QLabel()

        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__settings_struct = QSettings('openai_ini.ini', QSettings.IniFormat)
        api_key = self.__settings_struct.value('API_KEY', '')

        # load ini file
        self.__loadApiKeyInIni()

        # check if loaded API_KEY from ini file is not empty
        if openai.api_key:
            self.__setApiKey(api_key)
            self.__gptLLamaIndexClass = GPTLLamaIndexClass()
        # if it is empty
        else:
            self.__setAIEnabled(False)
            self.__apiCheckPreviewLbl.hide()

    def __initUi(self):
        self.setWindowTitle('PyQt LlamaIndex')

        self.__apiCheckPreviewLbl = QLabel()
        self.__apiCheckPreviewLbl.setFont(QFont('Arial', 10))

        apiLbl = QLabel('API')

        self.__apiLineEdit.setPlaceholderText('Write your API Key...')
        self.__apiLineEdit.returnPressed.connect(self.__setApi)
        self.__apiLineEdit.setEchoMode(QLineEdit.Password)

        apiBtn = QPushButton('Use')
        apiBtn.clicked.connect(self.__setApi)

        lay = QHBoxLayout()
        lay.addWidget(apiLbl)
        lay.addWidget(self.__apiLineEdit)
        lay.addWidget(apiBtn)
        lay.addWidget(self.__apiCheckPreviewLbl)
        lay.setContentsMargins(0, 0, 0, 0)

        apiWidget = QWidget()
        apiWidget.setLayout(lay)

        self.__listWidget = FileListWidget()
        self.__listWidget.clicked.connect(self.__setTextInBrowser)
        self.__listWidget.onDirectorySelected.connect(self.__onDirectorySelected)

        self.__prompt = Prompt()
        self.__lineEdit = self.__prompt.getTextEdit()
        self.__lineEdit.returnPressed.connect(self.__sendChat)
        self.__browser = ChatBrowser()
        
        lay = QVBoxLayout()
        lay.addWidget(self.__browser)
        lay.addWidget(self.__prompt)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        self.__txtBrowser = QTextBrowser()
        self.__txtBrowser.setPlaceholderText('This text browser shows selected file\'s content in the list.')
        self.__txtBrowser.setMaximumHeight(150)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        splitter = QSplitter()
        splitter.addWidget(self.__listWidget)
        splitter.addWidget(rightWidget)
        splitter.setChildrenCollapsible(False)
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(apiWidget)
        lay.addWidget(sep)
        lay.addWidget(splitter)
        lay.addWidget(self.__txtBrowser)
        lay.setAlignment(Qt.AlignTop)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.resize(800, 600)

    def __setApiKey(self, api_key):
        # for script
        openai.api_key = api_key
        # for subprocess (mostly)
        os.environ['OPENAI_API_KEY'] = api_key
        # for showing to the user
        self.__apiLineEdit.setText(api_key)

    def __loadApiKeyInIni(self):
        # this api key should be yours
        if self.__settings_struct.contains('API_KEY'):
            self.__setApiKey(self.__settings_struct.value('API_KEY'))
        else:
            self.__settings_struct.setValue('API_KEY', '')

    def __setAIEnabled(self, f):
        self.__prompt.setEnabled(f)

    def __setApi(self):
        try:
            api_key = self.__apiLineEdit.text()
            response = requests.get('https://api.openai.com/v1/engines', headers={'Authorization': f'Bearer {api_key}'})
            f = response.status_code == 200
            self.__setAIEnabled(f)
            if f:
                self.__setApiKey(api_key)
                self.__settings_struct.setValue('API_KEY', api_key)

                self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(0, 200, 0).name()))
                self.__apiCheckPreviewLbl.setText('API key is valid')
            else:
                raise Exception
        except Exception as e:
            self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(255, 0, 0).name()))
            self.__apiCheckPreviewLbl.setText('API key is invalid')
            self.__setAIEnabled(False)
            print(e)
        finally:
            self.__apiCheckPreviewLbl.show()

    def __onDirectorySelected(self):
        selected_dirname = self.__listWidget.getDir()
        self.__gptLLamaIndexClass.setDirectory(selected_dirname)

    def __sendChat(self):
        query_text = self.__lineEdit.toPlainText()
        self.__browser.showText(query_text, True)

        self.__lineEdit.setEnabled(False)

        self.__t = OpenAIThread(self.__gptLLamaIndexClass, query_text)
        self.__t.replyGenerated.connect(self.__browser.showText)
        self.__prompt.getTextEdit().clear()
        self.__t.start()
        self.__t.finished.connect(self.__afterGenerated)

    def __afterGenerated(self):
        self.__lineEdit.setEnabled(True)
        self.__lineEdit.setFocus()

    def __setTextInBrowser(self, txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            self.__txtBrowser.setText(f.read())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())



