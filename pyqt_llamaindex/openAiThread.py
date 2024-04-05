from PyQt5.QtCore import QThread, pyqtSignal


class OpenAIThread(QThread):
    """
    == replyGenerated Signal ==
    First: response
    Second: user or AI
    Third: streaming or not streaming
    """
    replyGenerated = pyqtSignal(str, bool, bool)
    streamFinished = pyqtSignal()

    def __init__(self, llama_idx_instance, query_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__llama_idx_instance = llama_idx_instance
        self.__query_text = query_text

    def run(self):
        try:
            response = self.__llama_idx_instance.getResponse(self.__query_text)
            self.replyGenerated.emit(response, False, False)
        except Exception as e:
            self.replyGenerated.emit(f'<p style="color:red">{e}</p>', False, False)