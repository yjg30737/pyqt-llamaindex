import os

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI


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

        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", streaming=True))

        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=512)
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

        self.__query_engine = index.as_query_engine(
            service_context=service_context,
            similarity_top_k=3,
            streaming=True
        )

    def getResponse(self, text):
        response = self.__query_engine.query(
            text,
        )

        return response

# BeautifulSoupWebReader
# DiscordReader
# GithubRepositoryReader