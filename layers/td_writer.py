from layers.writer import Writer

class TdWriter(Writer):
    def __init__(self, model='gpt-4-1106-preview'):
        system_prompt = f'生成测试因子'
        super().__init__(system_prompt)