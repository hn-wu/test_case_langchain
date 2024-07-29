from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import QianfanEmbeddingsEndpoint

def get_embedding(embedding: str, embedding_key: str=None,embedding_ak: str=None,embedding_sk: str=None):
    if embedding == 'm3e':
        return HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
    if embedding == "openai":
        return OpenAIEmbeddings(openai_api_key=embedding_key)
    if embedding == 'qianfan':
        return QianfanEmbeddingsEndpoint(qianfan_ak=embedding_ak, qianfan_sk=embedding_sk)
    else:
        raise ValueError(f"embedding {embedding} not support ")
