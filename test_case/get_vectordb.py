import os
from database.create_db import create_db,load_knowledge_db
from embeddings.call_embedding import get_embedding

def get_vectordb(file_path:str=None, persist_path:str=None, embedding="qianfan",embedding_key:dict=None):
    """
    返回向量数据库对象
    输入参数：
    embedding：可以使用zhipuai等embedding，不输入该参数则默认使用 qianfan embedding，注意此时api_key不要输错
    输出参数：
    vectordb:向量数据库(必要参数),一个对象
    """
    embedding = get_embedding(embedding=embedding, embedding_key=embedding_key)
    if os.path.exists(persist_path):  #持久化向量数据库目录
        contents = os.listdir(persist_path)
        if len(contents) == 0:  #但是下面为空
            #print("目录为空")
            vectordb = create_db(file_path, persist_path, embedding)
            #presit_knowledge_db(vectordb)
            vectordb = load_knowledge_db(persist_path, embedding)
        else:
            #print("目录不为空")
            vectordb = load_knowledge_db(persist_path, embedding)
    else: #目录不存在，从头开始创建向量数据库
        vectordb = create_db(file_path, persist_path, embedding)
        #presit_knowledge_db(vectordb)
        vectordb = load_knowledge_db(persist_path, embedding)

    return vectordb