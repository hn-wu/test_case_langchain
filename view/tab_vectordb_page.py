import gradio as gr
import random  # 导入random库，用于生成随机数
import time  # 导入time库，用于控制时间相关的功能


def tab_vectordb_page(config):
    """
    流程
    1. 检索知识库信息
    2. 增强回答
    """
    llm = config['llm']

    def get_writer():
        nonlocal llm
        llm = config['llm']
        if not llm:
            return None
        return llm.get_writer('vectordb')

    with gr.Tab("查询知识库") as tab:
        chatbot = gr.Chatbot()
        question = gr.Textbox(label="输入提问")  # 创建一个文本框组件，用于用户输入消息
        clear = gr.ClearButton([question, chatbot])  # 创建一个清除按钮，用于清除文本框和聊天机器人的内容

        def user(question, history):
            return "", history + [[question, None]]

        def chat(history):
            vectordb_writer = get_writer()
            question = history[-1][0]
            bot_message = vectordb_writer.chat_vectordb(question)
            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                yield history
            print(f"最终结果为：{history}")

        question.submit(user, [question, chatbot], [question, chatbot], queue=False).then(chat, chatbot, chatbot)
        clear.click(lambda: None, None, chatbot, queue=False)


