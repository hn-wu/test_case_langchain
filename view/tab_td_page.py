import os
import gradio as gr

from view.pipeline_Wrapper import Pipeline_Wrapper
from test_case.get_vectordb import get_vectordb

def tab_td_page(config):
    """
    流程
    1. 编写Story需求
    2. 以json格式返回缺陷知识库
    3. 存储缺陷知识库
    TODO
    1. 支持chatbot对缺陷知识库进行新增--更新--删除操作
    2. 存储聊天记录
    """

    llm = config['llm']

    def get_writer():
        nonlocal llm
        llm = config['llm']
        if not llm:
            return None
        return llm.get_writer('td')
    
    def get_inputs_text():
        td_writer = get_writer()
        return td_writer.get_input_context()

    def get_output_text():
        td_writer = get_writer()
        return td_writer.get_output()

    def on_submit(inputs):
        td_writer = get_writer()
        chat_outputs = ''
        for chat_output in td_writer.chat(question=inputs):
            chat_outputs += chat_output
        return chat_outputs

    def save():
        llm.save('td')
    
    with gr.Tab("创建缺陷知识库") as tab:
        with gr.Row():
            with gr.Column():
                placeholder = \
                """
                    需求名： 用户登录系统优化
                    需求价值： 提高用户登录体验，减少登录失败率，提升用户满意度和留存率
                    实现思路：
                    1. 增加社交账号一键登录功能（如微信、QQ、Facebook等）。
                    2. 优化登录界面和流程，提供友好的用户引导。
                    3. 增加忘记密码功能，方便用户找回密码。
                    4. 增加多因素认证（如短信验证码、邮箱验证码等）提升账户安全性。
                """
                inputs = gr.Textbox(label="说明你的Story需求", placeholder=placeholder, lines=10, interactive=True)
            output = gr.Textbox(label="生成的缺陷知识库", lines=10, interactive=True)
        start_button = gr.Button("开始")
        start_button.click(on_submit, [inputs], [output]).success(save)