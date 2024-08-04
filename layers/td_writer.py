from layers.writer import Writer

class TdWriter(Writer):

    def __init__(self, output_path, config):
        system_prompt = \
"""
你是一名测试人员，我会根据输入文档和需求，以JSON格式输出需求的的检查点和测试因子，但如果输入需求在文档中查询不到，返回查询失败。
输出格式：
{
"需求名": "<与输入的需求名一致>", // 这个键必须存在，用于分析/反思
"<检查点>": { // 对需求的需要检查的地方进行说明
"检查目的": "<填写检查的目的什么，对用户有什么叫做>",
"检查入参": "<填充检查的参数规范有哪些>",
"检查期望结果": "<在该字符串中编写检查点的期望结果>"  // 描述必须是一个字符串，不能为字典或列表
},
// 对需求需要检查的地方进行发散，列举出尽可能多的检查点，不要遗漏用户场景
}"""  
        super().__init__(output_path, config)
        
        self.td_content = {}
        self.details = ''
        self.load()
        self.update_system_prompt(system_prompt)
        
    def init_by_details(self, details):
        '''
        写入测试项目描述
        '''
        self.details = details
    
    def get_input_context(self):
        return self.details

    def get_output(self):
        return self.json_dumps(self.td_content)
    
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