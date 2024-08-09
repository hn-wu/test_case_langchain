import os
from test_case.chain_with_history import Client as ChatWithHistory
from test_case.chain_with_vectordb import Client as ChatWithVectordb
from common.untils import json_load, json_dumps, json_save

class Writer:
    def __init__(self, output_path, config):
        self.output_path = output_path
        self.config = config
        self.chat_history = []
        self.llm_history_client = self.init_llm_client(config=config)
        self.llm_vectordb_client = self.init_llm_vectordb_client(config=config)
        
    def init_llm_client(self,config):
        client = ChatWithHistory(
            model=config.get("model"),
            temperature=config.get("temperature"),
            top_k=config.get("top_k"),
            chat_history=self.chat_history,
            api_key=config.get("api_key"),
            wenxin_secret_key=config.get("wenxin_secret_key"),
            embedding=config.get("embedding"),
            embedding_key=config.get("embedding_key")
        )
        return client
    
    def init_llm_vectordb_client(self,config):
        client = ChatWithVectordb(
            model=config.get("model"),
            temperature=config.get("temperature"),
            top_k=config.get("top_k"),
            chat_history=self.chat_history,
            file_path=config.get("file_path"),
            persist_path=config.get("persist_path"),
            api_key=config.get("api_key"),
            wenxin_secret_key=config.get("wenxin_secret_key"),
            embedding=config.get("embedding"),
            embedding_key=config.get("embedding_key")
        )
        return client

    def update_system_prompt(self, system_prompt, out_prompt):
        chat_prompt = {
            "input": system_prompt,
            "output": out_prompt
        }
        self.llm_history_client.update_chat_prompt(chat_prompt)

    def update_llm_vectordb(self, file_path, persist_path):
        self.llm_history_client.update_vectordb(file_path=file_path, persist_path=persist_path)

    def update_llm_chat_history(self, chat_history):
        self.llm_history_client.update_history(chat_history)
    
    def update_config(self, **kwargs):
        self.config.update(**kwargs)
    
    def get_attrs_needed_to_save(self):
        raise NotImplementedError()

    def get_input_context(self) -> str:
        raise NotImplementedError
    
    def set_output(self, e):
        raise NotImplementedError
    
    def load(self, output_path=None):
        '''
        加载之前调用writer的入参
        '''
        if output_path is None: output_path = self.output_path
        attrs = self.get_attrs_needed_to_save()
        for attr, filename in attrs:
            attr_json_file = os.path.join(output_path, filename)
            if os.path.exists(attr_json_file):
                setattr(self, attr, json_load(attr_json_file))
    
    def save(self, output_path=None):
        '''
        保存当前调用writer的入参
        '''
        attrs = self.get_attrs_needed_to_save()
        if output_path is None: output_path = self.output_path
        os.makedirs(output_path, exist_ok=True)
        # 获得当前Writer对象对应值的索引；文件名
        for attr, filename in attrs:
            attr_json_file = os.path.join(output_path, filename)
            json_save(getattr(self, attr), attr_json_file)
    
    def get_chat_history(self, chat_id='main_chat', resume=True, inherit='system_messages'):
        if not resume or (chat_id not in self.chat_history):
            if inherit == 'system_messages':
                return [{'role':'system', 'content': self.chat_history['system_messages'][0]['content'] + self.get_input_context()}]
            else:
                return list(self.chat_history[inherit])
        else:
            return list(self.chat_history[chat_id])
    
    def get_model(self):
        return self.get_config('model')
    
    def chat(self, question):
        llm = self.llm_history_client
        yield from llm.answer(question)
        self.chat_history = self.llm_history_client.chat_history
    
    def chat_vectordb(self, question):
        llm = self.llm_vectordb_client
        yield from llm.answer(question)
        self.chat_vectordb_history = self.llm_vectordb_client.chat_history
    
    def json_dumps(self, json_object):
        return json_dumps(json_object)