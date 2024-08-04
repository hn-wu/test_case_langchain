from layers.writer import Writer

class TpWriter(Writer):

    def __init__(self, output_path, config):
        system_prompt = f'生成测试用例标题'
        super().__init__(output_path, config)
        self.tp_content = {}
        self.load()
        self.update_system_prompt(system_prompt)
    
    def init_by_td_writer(self, tp_writer):
        self.tp_writer = tp_writer
    
    def get_input_context(self):
        pass
    
    def get_attrs_needed_to_save(self):
        '''
        获得保存的文件列表
        params：
            td_content.json：生成的缺陷知识库
            td_chat_history.json：每个轮次大模型调用历史记录
            details.json：测试项目描述
        '''
        return [('tp_content', 'tp_content.json'), 
                ('chat_history', 'td_chat_history.json')]