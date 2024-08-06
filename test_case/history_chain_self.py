from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from test_case.model_to_llm import model_to_llm
from test_case.get_vectordb import get_vectordb
from test_case.chain_stream_handler import Client as ChainStreamHandler
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

import re

class Client():
    """"
    带历史记录的问答链  
    - model：调用的模型名称
    - temperature：温度系数，控制生成的随机性
    - top_k：返回检索的前k个相似文档
    - file_path：建库文件所在路径
    - persist_path：向量数据库持久化路径
    - api_key：所有模型都需要
    - wenxin_secret_key：文心秘钥
    - embeddings：使用的embedding模型  
    - embedding_key：使用的embedding模型的秘钥
    - wenxin_embedding_sk：文心使用的embedding模型的秘钥
    """
    def __init__(self,model:str, temperature:float=0.0, top_k:int=4, chat_history:list=[], 
                 file_path:str=None, persist_path:str=None, 
                 api_key:str=None, wenxin_secret_key:str=None, 
                 embedding="qianfan",embedding_key:dict=None):
        self.model = model
        self.temperature = temperature
        self.top_k = top_k
        self.chat_history = chat_history
        self.file_path = file_path
        self.persist_path = persist_path
        self.api_key = api_key
        self.wenxin_secret_key = wenxin_secret_key
        self.embedding = embedding
        self.embedding_key = embedding_key
        self.vectordb = get_vectordb(self.file_path, self.persist_path, self.embedding, self.embedding_key)
    

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
        # https://github.com/langchain-ai/langchain/discussions/13514
        # https://datawhalechina.github.io/llm-cookbook/#/C3/3.%20%E5%82%A8%E5%AD%98%20Memory
        # https://github.com/langchain-ai/langchain/issues/11975
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        if not self.chat_history:
            memory.save_context({"input": self.chat_prompt.get("input")}, {"output": self.chat_prompt.get("output")})
        chainStreamHandler = ChainStreamHandler()
        llm = model_to_llm(self.model, temperature, streaming, chainStreamHandler,
                           self.api_key, self.wenxin_secret_key)
        # 可以直接传入聊天历史 https://python.langchain.com.cn/docs/modules/chains/popular/chat_vector_db
        retriever = self.vectordb.as_retriever(search_type="similarity", search_kwargs={'k': top_k})
        # 设置prompt https://stackoverflow.com/questions/76175046/how-to-add-prompt-to-langchain-conversationalretrievalchain-chat-over-docs-with
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            retriever=retriever,
            memory=memory,
            callbacks=[chainStreamHandler])
        # 流式响应 https://www.langchain.cn/t/topic/138
        qa.invoke({"question": question})
        answer = ''
        for message in chainStreamHandler.generate_tokens():
            answer += message
            yield message
        self.save_stream_answer(question, answer, memory)

    def save_stream_answer(self, question, answer, memory):
        """"
        根据历史记录
        arguments: 
        - question：用户提问
        - answer：模型回答
        """
        answer = re.sub(r"\\n", '<br/>', answer)
        self.chat_history = memory.load_memory_variables({})["chat_history"]
        
















