import gradio as gr

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

    def set_output_text(chat_outputs):
        td_writer = get_writer()
        td_writer.set_output(chat_outputs)
        return get_output_text()

    def on_submit(inputs):
        td_writer = get_writer()
        chat_outputs = ''
        for chat_output in td_writer.chat(question=inputs):
            chat_outputs += chat_output
        chat_outputs = set_output_text(chat_outputs)
        return chat_outputs

    def save():
        llm.save('td')
    
    with gr.Tab("创建缺陷知识库") as tab:
        with gr.Row():
            with gr.Column():
                placeholder = \
"""
需求名： 命令行配置聚合口
需求价值： 简化聚合口配置
需求验收条件：
1. 输入ip、netmask、mtu、聚合口成员、聚合模式
2. 支持创建、修改、删除聚合口
3. 不同主机之间聚合口正常连通
"""
                inputs = gr.Textbox(label="说明你的Story需求", placeholder=placeholder, lines=10, interactive=True)
            output = gr.Textbox(label="生成的缺陷知识库", lines=10, interactive=True)
        start_button = gr.Button("开始")
        start_button.click(on_submit, [inputs], [output]).success(save)