import inspect

import openai

from PyQt5.QtCore import QThread, pyqtSignal


class OpenAIThread(QThread):
    replyGenerated = pyqtSignal(str, bool)
    streamFinished = pyqtSignal()

    def __init__(self, llama_idx_instance, query_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__llama_idx_instance = llama_idx_instance
        self.__query_text = query_text

    def run(self):
        try:
            streaming_response = self.__llama_idx_instance.getResponse(self.__query_text)
            for response_text in streaming_response.response_gen:
                self.replyGenerated.emit(response_text, False)
        except openai.error.InvalidRequestError as e:
            print(e)
            self.replyGenerated.emit('<p style="color:red">Your request was rejected as a result of our safety system.<br/>'
                                     'Your prompt may contain text that is not allowed by our safety system.</p>', False)
        except openai.error.RateLimitError as e:
            self.replyGenerated.emit(f'<p style="color:red">{e}<br/>Check the usage: https://platform.openai.com/account/usage<br/>Update to paid account: https://platform.openai.com/account/billing/overview', False)