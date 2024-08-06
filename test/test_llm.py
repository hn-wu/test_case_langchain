from langchain_community.llms import QianfanLLMEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

model = "ERNIE-Speed-128K"
api_key = "clLcz3pG0KETHqhDkFUURfSn"  # API密钥
wenxin_secret_key = "kjmDsDF73j5LnCW2LADz2EIOreYHtaGS"  # 文心秘钥
llm = QianfanLLMEndpoint(model=model, temperature=0.9, qianfan_ak=api_key, qianfan_sk=wenxin_secret_key)
memory = ConversationBufferMemory()

# 首先，构造一个提示模版字符串：`template_string`
template_string = """把由三个反引号分隔的文本\
翻译成一种{style}风格。\
文本: ```{text}```
"""

# 然后，我们调用`ChatPromptTemplatee.from_template()`函数将
# 上面的提示模版字符`template_string`转换为提示模版`prompt_template`

prompt_template = ChatPromptTemplate.from_template(template_string)
conversation = ConversationChain(llm=llm, memory = memory, verbose=True )

# 直接添加内存
system_prompt = \
    """
    你是一名测试人员，能根据输入文档和需求，以JSON格式输出需求的的检查点和测试因子，但如果输入需求在文档中查询不到，返回查询失败。
    输出格式：
    {
    "需求名": "<与输入的需求名一致>", // 这个键必须存在，用于分析/反思
    "检查点": { // 对需求的需要检查的地方进行说明
    "检查目的": "<填写检查的目的什么，对用户有什么价值>",
    "检查入参": "<填充检查的参数规范有哪些>",
    "检查期望结果": "<在该字符串中编写检查点的期望结果>"  // 描述必须是一个字符串，不能为字典或列表
    },
    // 对需求需要检查的地方进行发散，列举出尽可能多的检查点，不要遗漏用户场景
    }"""  
memory.save_context({"input": system_prompt}, {"output": "好的，我明白了。现在，请您提供具体的输入文档和需求，我会根据这些信息为您生成相应的JSON格式检查点和测试因子。"})
memory.load_memory_variables({})

story = \
    """
    需求名： 用户登录系统优化
    需求价值： 提高用户登录体验，减少登录失败率，提升用户满意度和留存率
    实现思路：

    增加社交账号一键登录功能（如微信、QQ、Facebook等）。
    优化登录界面和流程，提供友好的用户引导。
    增加忘记密码功能，方便用户找回密码。
    增加多因素认证（如短信验证码、邮箱验证码等）提升账户安全性。
    """
conversation.predict(input=story)

memory.load_memory_variables({})