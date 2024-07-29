import time
import sys
from typing import Generator
from langchain.callbacks import StreamingStdOutCallbackHandler

class Client(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)

    def generate_tokens(self) -> Generator:
        while not self.finish:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                self.finish = True
                time.sleep(0.2)