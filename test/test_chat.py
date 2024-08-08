from test_case.chain_with_vectordb import Client as ChatWithVectordb

# 定义必要的参数
model = "ERNIE-Speed-128K"  # 使用的模型名称
temperature = 0.1  # 控制生成的随机性
top_k = 5  # 返回检索的前k个相似文档
file_path = "../knowledge_db/prompt_engineering"  # 向量数据库文件路径
persist_path = "../vector_db/chroma"  # 向量数据库持久化路径
api_key = "clLcz3pG0KETHqhDkFUURfSn"  # API密钥
wenxin_secret_key = "kjmDsDF73j5LnCW2LADz2EIOreYHtaGS"  # 文心秘钥
embedding = "qianfan"  # 使用的嵌入模型
# 嵌入模型的密钥
embedding_key = {
    "qianfan_ak":"clLcz3pG0KETHqhDkFUURfSn",
    "qianfan_sk":"kjmDsDF73j5LnCW2LADz2EIOreYHtaGS",
    }

# 创建带有历史记录的问答链客户端
client = ChatWithVectordb(
    model=model,
    temperature=temperature,
    top_k=top_k,
    file_path=file_path,
    persist_path=persist_path,
    api_key=api_key,
    wenxin_secret_key=wenxin_secret_key,
    embedding=embedding,
    embedding_key=embedding_key,
)
system_prompt = \
    """
    你是一名测试人员，我会根据输入文档和需求，以JSON格式输出需求的的检查点和测试因子
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
out_prompt = "好的，我明白了。现在，请您提供具体的输入文档和需求，我会根据这些信息为您生成相应的JSON格式检查点和测试因子。"  
chat_prompt = {
    "input": system_prompt,
    "output": out_prompt
}
client.update_chat_prompt(chat_prompt)

# 示例对话
question1 = \
    """
    需求名： 用户登录系统优化
    需求价值： 提高用户登录体验，减少登录失败率，提升用户满意度和留存率
    实现思路：

    增加社交账号一键登录功能（如微信、QQ、Facebook等）。
    优化登录界面和流程，提供友好的用户引导。
    增加忘记密码功能，方便用户找回密码。
    增加多因素认证（如短信验证码、邮箱验证码等）提升账户安全性。
    """
print("Q: ", question1)
answer = ''
for partial_answer in client.answer(question1):
    answer += partial_answer
    print(partial_answer, end='')

