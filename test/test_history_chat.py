from test_case.history_chain_self import Client as HistoryChat

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
client = HistoryChat(
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

# 示例对话
question1 = "我可以学习到关于提示工程的知识吗？"
print("Q: ", question1)
answer = ''
for partial_answer in client.answer(question1):
    answer += partial_answer
    print(partial_answer, end='')
client.save_stream_answer(question1,answer)

# 下一个问题，可以根据历史记录产生更好的回答
question2 = "如果学不了提示工程，那是为什么；如果可以学到，给出学习路线"
print("Q: ", question2)
answer = ''
for partial_answer in client.answer(question2):
    answer += partial_answer
    print(partial_answer, end='') 
client.save_stream_answer(question1,answer)

