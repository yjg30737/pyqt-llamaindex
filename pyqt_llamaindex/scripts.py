import os

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


class GPTLLamaIndexClass:
    def __init__(self):
        self.__initVal()
        self.__init()

    def __initVal(self):
        self.__directory = './example'

    def setDirectory(self, directory):
        self.__directory = directory

    def __init(self):
        documents = SimpleDirectoryReader(self.__directory).load_data()
        index = VectorStoreIndex.from_documents(documents)

        self.__query_engine = index.as_query_engine()

    def getResponse(self, text):
        try:
            resp = self.__query_engine.query(
                text,
            )
            return resp.response
        except Exception as e:
            return str(e)

# BeautifulSoupWebReader
# DiscordReader
# GithubRepositoryReader