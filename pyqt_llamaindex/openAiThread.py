from PyQt5.QtCore import QThread, pyqtSignal
from llama_index.core.base.response.schema import StreamingResponse


class OpenAIThread(QThread):
    """
    == replyGenerated Signal ==
    First: response
    Second: user or AI
    Third: streaming or not streaming
    """
    replyGenerated = pyqtSignal(str, bool, bool)
    streamFinished = pyqtSignal()

    def __init__(self, wrapper, query_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__wrapper = wrapper
        self.__query_text = query_text

    def run(self):
        try:
            resp = self.__wrapper.get_response(self.__query_text)
            f = isinstance(resp, StreamingResponse)
            if f:
                for chunk in resp.response_gen:
                    self.replyGenerated.emit(chunk, True, True)
            else:
                self.replyGenerated.emit(resp.response, False, False)
        except Exception as e:
            self.replyGenerated.emit(f'<p style="color:red">{e}</p>', False, False)