from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import QianfanLLMEndpoint
from langchain_community.llms import Ollama


def model_to_llm(model:str=None, temperature:float=0.0, streaming:bool=True, chainStreamHandler:object=None,
                 api_key:str=None, wenxin_secret_key:str=None):
        """
        百度问心：model,temperature,api_key,api_secret
        OpenAI：model,temperature,api_key
        """
        if model in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0613", "gpt-4", "gpt-4-32k"]:
            llm = ChatOpenAI(model_name = model, temperature = temperature , openai_api_key = api_key,
                             callbacks=[chainStreamHandler])
        elif model in ["ERNIE-Bot", "ERNIE-Bot-4", "ERNIE-Bot-turbo","ERNIE-Speed-128K"]:
            if streaming:
                llm = QianfanLLMEndpoint(model=model, temperature = temperature, 
                                        streaming=True, callbacks=[chainStreamHandler],
                                        qianfan_ak=api_key, qianfan_sk=wenxin_secret_key)
            else:
                llm = QianfanLLMEndpoint(model=model, temperature = temperature, streaming=False, 
                                        qianfan_ak=api_key, qianfan_sk=wenxin_secret_key)
        elif model in ['qwen2:7b']:
             llm = Ollama(model=model)
        else:
            raise ValueError(f"model{model} not support!!!")
        return llm