from layers.writer import Writer
from common.untils import json_load, json_dumps
import json

class TdWriter(Writer):

    def __init__(self, output_path, config):
        super().__init__(output_path, config)

        system_prompt = """
你是一名测试人员，会根据输入文档和需求，并以json格式输出需求的的检查点和测试因子，注意在回复中不要复述问题
接来下我会输入需求名和验收条件，你需要对需求检查点进行发散，列举出尽可能多的检查点，包括正常场景和异常场景，不要出现遗漏
输出格式：
```json
{
"需求名": "<与输入的需求名一致>", // 这个键必须存在，用于分析/反思
"<检查点>": { // 对需求的需要检查的地方进行说明
"检查目的": "<填写检查的目的什么，对用户有什么叫做>",
"检查入参": "<填充检查的参数规范有哪些>",
"检查期望结果": "<在该字符串中编写检查点的期望结果>"  // 描述必须是一个字符串，不能为字典或列表
},
```
"""  
        out_prompt = "好的，我明白了，我会将接受需求名和验收条件，对检查点进行发散，并以json格式输出"
        self.td_content = {}
        self.details = ''
        self.load()
        self.update_system_prompt(system_prompt, out_prompt)
        
    def init_by_details(self, details):
        '''
        写入测试项目描述
        '''
        self.details = details
    
    def get_input_context(self):
        return self.details

    def get_output(self):
        if isinstance(self.td_content, dict):
            return self.json_dumps(self.td_content)
        else:
            return "td_content返回值不为json格式"

    def set_output(self, td_content):
        try:
            td_content = json.loads(td_content.split("```")[1][5:-1])
            assert isinstance(td_content, dict), 'set_output:The type of outline must be dict!'
            self.td_content = td_content
        except Exception as e:
            return "td_content返回值不为json格式"
    
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