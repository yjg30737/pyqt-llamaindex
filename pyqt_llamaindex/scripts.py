import os

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


class LlamaIndexWrapper:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._directory: str = "./example"
        self._query_engine = None
        self._index = None
        self.set_directory(self._directory)

    def set_directory(
            self,
            directory: str,
            ext: list[str] | None = None,
    ) -> None:
        if not ext:
            default_ext = [".txt"]
            ext = default_ext if default_ext else []
        assert ext, "llama_index_supported_formats is not set"
        self._directory = directory
        documents = SimpleDirectoryReader(
            input_dir=self._directory,
            required_exts=ext,
        ).load_data()
        self._index = VectorStoreIndex.from_documents(documents)

    def is_query_engine_set(self) -> bool:
        return self._query_engine is not None

    def set_query_engine(
        self,
        streaming: bool = False,
        similarity_top_k: int = 3,
    ):
        if self._index is None:
            raise Exception(
                "Index must be initialized first. Call set_directory or set_files first.",
            )
        try:
            self._query_engine = self._index.as_query_engine(
                streaming=streaming,
                similarity_top_k=similarity_top_k,
            )
            print("Set query engine")
        except Exception as e:
            raise Exception("Error in setting query engine") from e

    def get_directory(self) -> str:
        """This function returns the directory path.
        If directory does not exist, it will return the empty string.
        """
        return (
            self._directory
            if self._directory and os.path.exists(self._directory)
            else ""
        )

    def get_response(self, text: str):
        try:
            if self._query_engine:
                resp = self._query_engine.query(
                    text,
                )
                return resp
            raise Exception(
                "Query engine not initialized. Maybe you need to set the directory first. Check the directory path.",
            )
        except Exception as e:
            return str(e)

# BeautifulSoupWebReader
# DiscordReader
# GithubRepositoryReader