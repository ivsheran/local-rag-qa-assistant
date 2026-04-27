import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


class RAGChain:
    def __init__(self, config, vector_store):
        self.config = config
        self.vector_store = vector_store
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, "prompts", "qa_prompt.txt")
        self.prompt = PromptTemplate.from_template(self._load_prompt(prompt_path))
        self.sessions = {}

    def _load_prompt(self, prompt_path):
        with open(prompt_path, "r") as f:
            return f.read()

    def get_memory(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = InMemoryChatMessageHistory()
        return self.sessions[session_id]

    def build_chain(self, model_name):
        llm = ChatOllama(model=model_name, base_url=self.config.ollama_base_url)
        chain = self.prompt | llm | StrOutputParser()
        return RunnableWithMessageHistory(
            chain,
            self.get_memory,
            input_messages_key="question",
            history_messages_key="history"
        )
