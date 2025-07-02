from langchain.chains import LLMChain
#from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama

from config import settings


class BaseStructureChain:

    PROMPT = ""

    def __init__(self) -> None:

        self.llm = ChatOllama(model=settings["model"], base_url=settings["baseurl"])

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True


class BaseEventChain:

    PROMPT = ""

    def __init__(self) -> None:

        self.llm = ChatOllama(model=settings["model"], base_url=settings["baseurl"])

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True
