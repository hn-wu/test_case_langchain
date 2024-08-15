import instructor
from pydantic import BaseModel
from openai import OpenAI
from typing import List
import instructor

model='qwen2:7b'

client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="NA",  # required, but unused
    ),
    mode = instructor.Mode.JSON,
)

#结构化输出
class UserDetail(BaseModel):
    name: str
    age: int
    hobby: List[str]
    
#Prompt提示
PROMPT_TEXT = "根据自我介绍文本内容，从中提取出姓名、年龄、兴趣"

#实验数据
introduction_text = '我是张三，今年34岁， 来自黑龙江省， 我的兴趣爱好有打篮球、踢足球、游泳、打游戏。'

# 参考 https://jxnl.github.io/instructor/#calling-create
resp = client.chat.completions.create(
    model = "qwen2:7b",
    messages=[{"role": "system", "content": PROMPT_TEXT},{"role": "user", "content": introduction_text}],
    response_model = UserDetail,
    max_retries = 3
)

print(resp.model_dump_json(indent=2))