from layers.writer import Writer

class CaseWriter(Writer):
    def __init__(self, output_path, config):
        system_prompt = f'生成测试用例步骤，组成完整的测试用例'
        super().__init__(system_prompt, output_path, config)
        self.case_content = {}
        self.load()

    def init_by_td_and_tp_writer(self, td_writer, tp_writer):
        self.td_writer = td_writer
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
        return [('case_content', 'case_content.json'), 
                ('chat_history', 'case_chat_history.json')]