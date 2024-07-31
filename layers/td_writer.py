from layers.writer import Writer

class TdWriter(Writer):

    def __init__(self, output_path, config):
        system_prompt = f'生成测试因子'
        super().__init__(system_prompt, output_path, config)
        
        self.td_content = {}
        self.details = ''
        self.load()
        
    def init_by_details(self, details):
        '''
        写入测试项目描述
        '''
        self.details = details
    
    def get_input_context(self):
        return self.details
    
    def get_attrs_needed_to_save(self):
        '''
        获得保存的文件列表
        params：
            td_content.json：生成的缺陷知识库
            td_chat_history.json：每个轮次大模型调用历史记录
            details.json：测试项目描述
        '''
        return [('td_content', 'td_content.json'), 
                ('chat_history', 'td_chat_history.json'), 
                ('details', 'details.json')]