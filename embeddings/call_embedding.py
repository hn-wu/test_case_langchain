from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import QianfanEmbeddingsEndpoint

def get_embedding(embedding: str, embedding_key: dict=None):
    if embedding == "openai":
        return OpenAIEmbeddings(openai_api_key=embedding_key["embedding_key"])
    elif embedding == 'qianfan':
        return QianfanEmbeddingsEndpoint(qianfan_ak=embedding_key["qianfan_ak"], 
                                         qianfan_sk=embedding_key["qianfan_sk"])
    else:
        raise ValueError(f"embedding {embedding} not support ")
