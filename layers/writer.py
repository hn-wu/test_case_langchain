import os
from test_case.history_chain_self import Client as HistoryChat
from common.untils import json_load, json_dumps, json_save

class Writer:
    def __init__(self, output_path, config):
        self.output_path = output_path
        self.config = config
        self.chat_history = []
        self.llm_client = self.init_llm_client(config=config)
        
    def init_llm_client(self,config):
        client = HistoryChat(
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
        self.llm_client.update_chat_prompt(chat_prompt)

    def update_llm_vectordb(self, file_path, persist_path):
        self.llm_client.update_vectordb(file_path=file_path, persist_path=persist_path)

    def update_llm_chat_history(self, chat_history):
        self.llm_client.update_history(chat_history)
    
    def update_config(self, **kwargs):
        self.config.update(**kwargs)
    
    def get_attrs_needed_to_save(self):
        raise NotImplementedError()

    def get_input_context(self) -> str:
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
        llm = self.llm_client
        yield from llm.answer(question)

    def discuss(self, prompt):
        messages = self.get_chat_history()
        messages.append({'role':'user', 'content': prompt})  
        response_msgs = yield from self.chat(messages, response_json=False)
        context_messages = response_msgs
        self.update_chat_history(context_messages)
        yield context_messages
    
    def json_dumps(self, json_object):
        return json_dumps(json_object)