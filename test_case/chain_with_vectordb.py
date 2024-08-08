from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from test_case.model_to_llm import model_to_llm
from test_case.get_vectordb import get_vectordb
from test_case.chain_stream_handler import ChainStreamHandler
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain

class Client():
    """"
    带历史记录的问答链，结合RAG进行增强  
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
    TODO
    1. ConversationalRetrievalChain 和 ConversationSummaryBufferMemory 不能适配问题【输入问题会被question_generator重新总结】
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
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.memory = memory

    def update_chat_prompt(self, chat_prompt):
        self.chat_prompt = chat_prompt

    def update_vectordb(self, file_path:str=None, persist_path:str=None):
        self.vectordb = get_vectordb(file_path, persist_path, self.embedding, self.embedding_key)

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

        chainStreamHandler = ChainStreamHandler()
        llm = model_to_llm(self.model, temperature, False, api_key=self.api_key, wenxin_secret_key=self.wenxin_secret_key)
        streaming_llm  = model_to_llm(self.model, temperature, streaming, chainStreamHandler, self.api_key, self.wenxin_secret_key)
        # 问题补充
        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        # 回答生成
        doc_chain = load_qa_chain(streaming_llm, chain_type="stuff", prompt=QA_PROMPT)       
        # 可以直接传入聊天历史 https://python.langchain.com.cn/docs/modules/chains/popular/chat_vector_db
        retriever = self.vectordb.as_retriever(search_type="similarity", search_kwargs={'k': top_k})
        # 设置prompt https://stackoverflow.com/questions/76175046/how-to-add-prompt-to-langchain-conversationalretrievalchain-chat-over-docs-with
        qa = ConversationalRetrievalChain(
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
            retriever=retriever,
            memory=self.memory)
        # 流式响应 https://www.langchain.cn/t/topic/138
        qa.invoke({"question": question})
        for message in chainStreamHandler.generate_tokens():
            yield message
        
















