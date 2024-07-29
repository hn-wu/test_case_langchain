from layers.writer import Writer

class CaseWriter(Writer):
    def __init__(self, model='gpt-4-1106-preview'):
        system_prompt = f'生成测试用例步骤，组成完整的测试用例'
        super().__init__(system_prompt)

    def init_by_td_and_tp_writer(self, td_writer, tp_writer):
        self.td_writer = td_writer
        self.tp_writer = tp_writer