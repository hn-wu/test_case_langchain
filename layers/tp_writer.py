from layers.writer import Writer

class TpWriter(Writer):

    def __init__(self, model='gpt-4-1106-preview'):
        system_prompt = f'生成测试用例标题'
        super().__init__(system_prompt)
    
    def init_by_td_writer(self, tp_writer):
        self.tp_writer = tp_writer