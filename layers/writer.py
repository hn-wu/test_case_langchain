import os
from test_case.history_chain_self import Client as HistoryChat
from common.untils import json_load, json_dumps, json_save

class Writer:
    def __init__(self, system_prompt, output_path, config):
        self.output_path = output_path
        self.config = config
        self.system_prompt = system_prompt
        self.chat_history = {
            'system_messages': [{'role':'system', 'content': system_prompt}],
            }
    
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
    
    def chat(self):
        """
        调用大模型
        """
        pass