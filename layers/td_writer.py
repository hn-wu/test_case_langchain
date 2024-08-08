from layers.writer import Writer
from common.untils import json_load, json_dumps
import json

class TdWriter(Writer):

    def __init__(self, output_path, config):
        super().__init__(output_path, config)

        system_prompt = """
你是一名测试人员，会根据输入文档和需求，并以特定的格式输出需求的的检查点和测试因子，注意在回复中不要复述问题
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
        out_prompt = """
好的，我明白了，输出结果:
```json
{  
    "需求名": "用户注册功能",  
    "用户名检查": {  
        "检查目的": "确保用户输入的用户名符合规范，避免非法字符和重复注册",  
        "检查入参": "用户名需为6-20位字母、数字或下划线组成，不能为空且唯一",  
        "检查期望结果": "用户名输入正确时，注册成功；输入为空、包含非法字符或已存在时，显示相应的错误提示"  
    },  
    "密码检查": {  
        "检查目的": "确保用户输入的密码足够安全，符合密码复杂度要求",  
        "检查入参": "密码需为8-20位，包含大小写字母、数字和特殊字符中的至少三种",  
        "检查期望结果": "密码输入符合规范时，注册成功；不符合时，显示相应的错误提示"  
    },  
    "确认密码检查": {  
        "检查目的": "确保用户两次输入的密码一致",  
        "检查入参": "用户需再次输入密码以确认，两次输入的密码必须完全一致",  
        "检查期望结果": "两次输入的密码一致时，注册成功；不一致时，显示密码不一致的错误提示"  
    },  
    "邮箱检查": {  
        "检查目的": "确保用户输入的邮箱地址格式正确且唯一",  
        "检查入参": "邮箱地址需符合标准邮箱格式，且未被其他用户注册",  
        "检查期望结果": "邮箱输入正确且唯一时，注册成功；格式错误或已存在时，显示相应的错误提示"  
    },  
    "手机号检查": {  
        "检查目的": "确保用户输入的手机号格式正确且唯一",  
        "检查入参": "手机号需为11位数字，且未被其他用户注册",  
        "检查期望结果": "手机号输入正确且唯一时，注册成功；格式错误或已存在时，显示相应的错误提示"  
    },  
    "验证码检查": {  
        "检查目的": "确保用户输入的验证码正确",  
        "检查入参": "用户需输入接收到的验证码，验证码需在有效期内且正确",  
        "检查期望结果": "验证码输入正确时，注册成功；验证码错误或过期时，显示相应的错误提示"  
    },  
    "注册协议同意检查": {  
        "检查目的": "确保用户已阅读并同意注册协议",  
        "检查入参": "用户需勾选同意注册协议",  
        "检查期望结果": "用户勾选同意协议后，注册成功；未勾选时，显示未同意协议的错误提示"  
    },  
    "注册后用户信息检查": {  
        "检查目的": "验证注册后用户信息是否正确保存",  
        "检查入参": "用户注册成功后，系统应保存用户的注册信息",  
        "检查期望结果": "用户注册成功后，能够在系统中查询到正确的用户信息"  
    }  
}
```
"""   
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
            return self.td_content
        return self.json_dumps(self.td_content)

    def set_output(self, td_content):
        try:
            td_content = json.loads(td_content.split("```")[1][5:-1])
            assert isinstance(td_content, dict), 'set_output:The type of outline must be dict!'
            self.td_content = td_content
        except Exception as e:
            raise ValueError("td_content返回值不为json格式")
    
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