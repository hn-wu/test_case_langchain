import time
import sys
from typing import Generator
from langchain.callbacks import StreamingStdOutCallbackHandler

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        # 记得结束后这里置true
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)

    def on_llm_end(self, response, **kwargs) -> None:
        self.finish = 1

    def generate_tokens(self) -> Generator:
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                time.sleep(1)