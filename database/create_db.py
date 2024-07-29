import os
import re
import tempfile
from embeddings.call_embedding import get_embedding
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

DEFAULT_DB_PATH = "../knowledge_db"
DEFAULT_PERSIST_PATH = "../vector_db"

def create_db(folder_path=DEFAULT_DB_PATH, persist_directory=DEFAULT_PERSIST_PATH, embeddings="qianfan"):
    """
    该函数用于加载 PDF 文件，切分文档，生成文档的嵌入向量，创建向量数据库。
    参数:
    file: 存放文件的路径。
    embeddings: 用于生产 Embedding 的模型
    返回:
    vectordb: 创建的数据库。
    """
    if folder_path == None:
        return "can't load empty file"
    file_list = get_files(folder_path)
    loaders = []
    [file_loader(file, loaders) for file in file_list]
    docs = []
    for loader in loaders:
        if loader is not None:
            docs.extend(loader.load())
    # 切分文档
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    if type(embeddings) == str:
        embeddings = get_embedding(embedding=embeddings)
    # 加载数据库
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory  # 允许我们将persist_directory目录持久化存储
    ) 

    vectordb.persist()
    return vectordb


def load_knowledge_db(path, embeddings):
    """
    该函数用于加载向量数据库。

    参数:
    path: 要加载的向量数据库路径。
    embeddings: 向量数据库使用的 embedding 模型。

    返回:
    vectordb: 加载的数据库。
    """
    vectordb = Chroma(
        persist_directory=path,
        embedding_function=embeddings
    )
    return vectordb

def presit_knowledge_db(vectordb):
    """
    该函数用于持久化向量数据库。

    参数:
    vectordb: 要持久化的向量数据库。
    """
    vectordb.persist()

def get_files(dir_path):
    file_list = []
    for filepath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            file_list.append(os.path.join(filepath, filename))
    return file_list


def file_loader(file, loaders):
    if isinstance(file, tempfile._TemporaryFileWrapper):
        file = file.name
    if not os.path.isfile(file):
        [file_loader(os.path.join(file, f), loaders) for f in  os.listdir(file)]
        return
    file_type = file.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file))
    elif file_type == 'md':
        pattern = r"敏感词|禁止查询"
        match = re.search(pattern, file)
        if not match:
            loaders.append(TextLoader(file,encoding="utf-8"))
    elif file_type == 'txt':
        loaders.append(UnstructuredFileLoader(file))
    return

if __name__ == "__main__":
    create_db(embeddings="m3e")
