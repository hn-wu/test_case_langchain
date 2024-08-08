from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from test_case.model_to_llm import model_to_llm
from test_case.get_vectordb import get_vectordb
from test_case.chain_stream_handler import ChainStreamHandler
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.question_answering import load_qa_chain

class Client():
    """"
    带历史记录的问答链，但不使用RAG  
    - model：调用的模型名称
    - temperature：温度系数，控制生成的随机性
    - top_k：返回检索的前k个相似文档
    - api_key：所有模型都需要
    - wenxin_secret_key：文心秘钥
    - embeddings：使用的embedding模型  
    - embedding_key：使用的embedding模型的秘钥
    - wenxin_embedding_sk：文心使用的embedding模型的秘钥
    TODO
    1. ConversationalRetrievalChain 和 ConversationSummaryBufferMemory 不能适配问题【输入问题会被question_generator重新总结】
    """
    def __init__(self,model:str, temperature:float=0.0, top_k:int=4, chat_history:list=[], 
                 api_key:str=None, wenxin_secret_key:str=None, 
                 embedding="qianfan",embedding_key:dict=None):
        self.model = model
        self.temperature = temperature
        self.top_k = top_k
        self.chat_history = chat_history
        self.api_key = api_key
        self.wenxin_secret_key = wenxin_secret_key
        self.embedding = embedding
        self.embedding_key = embedding_key
        memory = ConversationBufferMemory(memory_key="history", return_messages=True)
        self.memory = memory

    def update_chat_prompt(self, chat_prompt):
        self.chat_prompt = chat_prompt

    def update_vectordb(self, file_path:str=None, persist_path:str=None):
        self.vectordb = get_vectordb(file_path, persist_path, self.embedding, self.embedding_key)

    def update_history(self, chat_history):
        "更新历史记录"
        self.chat_history = chat_history

    def clear_history(self):
        "清空历史记录"
        return self.chat_history.clear()
    
    def change_history_length(self,history_len:int=1):
        """
        保存指定对话轮次的历史记录
        输入参数：
        - history_len ：控制保留的最近 history_len 次对话
        - chat_history：当前的历史对话记录
        输出：返回最近 history_len 次对话
        """
        save_count = len(self.chat_history) - history_len
        return self.chat_history[save_count:]

    def answer(self, question:str=None,temperature = None, top_k = 4, streaming=True):
        """"
        核心方法，调用问答链
        arguments: 
        - question：用户提问
        """
        if len(question) == 0:
            return "", self.chat_history
        if len(question) == 0:
            return ""
        if temperature == None:
            temperature = self.temperature

        # 设置SystemMessage和chat_history
        # https://github.com/langchain-ai/langchain/discussions/4199
        # https://github.com/langchain-ai/langchain/discussions/13514
        # https://datawhalechina.github.io/llm-cookbook/#/C3/3.%20%E5%82%A8%E5%AD%98%20Memory
        # https://github.com/langchain-ai/langchain/issues/11975
        # ConversationalRetrievalChain 和 ConversationSummaryBufferMemory
        # https://github.com/langchain-ai/langchain/issues/2303
        if not self.chat_history:
            self.memory.save_context({"input": self.chat_prompt.get("input")}, {"output": self.chat_prompt.get("output")})
        chainStreamHandler = ChainStreamHandler()
        streaming_llm  = model_to_llm(self.model, temperature, streaming, chainStreamHandler, self.api_key, self.wenxin_secret_key)
        # 设置prompt https://stackoverflow.com/questions/76175046/how-to-add-prompt-to-langchain-conversationalretrievalchain-chat-over-docs-with
        # verbose参数设置为True时，程序会输出更详细的信息，以提供更多的调试或运行时信息。
        qa = ConversationChain(
            llm=streaming_llm,
            memory=self.memory,
            verbose=True)
        # 流式响应 https://www.langchain.cn/t/topic/138
        qa.invoke({"input": question})
        for message in chainStreamHandler.generate_tokens():
            yield message
        self.chat_history = self.memory.load_memory_variables({})["history"]
        
















