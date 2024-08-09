import os
import gradio as gr

from view.pipeline_Wrapper import Pipeline_Wrapper
from test_case.get_vectordb import get_vectordb

def tab_main_page(config):
    """
    流程
    1. 创建测试活动
    2. 输入描述
    3. 点击创建测试活动【创建chat history记录】
    4. 加载测试活动
    5. 上传文档
    6. 点击开始测试【创建向量数据库】
    """

    def create_option(e):
        '''
        选择栏，选择你要做的操作是什么
        return
            option：你选择的操作
        '''
        return gr.Radio(label='选择操作', choices=['新建测试活动', '加载测试活动'], value=e)

    def get_available_input_options():
        input_options = []
        if not os.path.exists("../chathistory"):
            os.makedirs("../chathistory")
        for name in os.listdir("../chathistory"):
            if os.path.isdir(os.path.join("../chathistory", name)):
                input_options.append(name)
        return input_options

    with gr.Tab("选择测试活动") as tab:
        '''
        return
            option[组件]:输入的操作['新建测试活动', '加载测试活动']
            input_optins[组件]:选择你加载的测试活动
            submit_create[组件]:点击按钮创建测试项目
            inputs[组件]:新建的测试活动
            details[组件]:传入文档【选择加载测试活动后才会显示】
            submit_start[组件]:点击按钮开始测试
        '''
        option = create_option('')
        input_options = gr.Radio(label='', choices=[])
        inputs = gr.Textbox(label='', value='', lines=1, interactive=False)
        details = gr.Textbox(label="简答描述一下测试活动", lines=4, placeholder="可以选择在这里输入更多细节", interactive=True)
        submit_create = gr.Button("创建或修改测试活动")
        files = gr.Files()
        submit_start = gr.Button("开始测试")
    
    def load_input_options(e=''):
        '''
        返回之前创建的测试活动
        '''
        input_options = get_available_input_options()
        return gr.Radio(label='加载已有测试活动', choices=input_options, value=e)

    def on_select_option(evt: gr.SelectData):
        '''
        选择不同的选项，返回不同的前端输入组件
        '''
        if evt.value == '加载测试活动':
            return load_input_options(''), gr.Textbox(label='', value='', interactive=False)
        else:
            return gr.Radio(label='', choices=[]), gr.Textbox(label="输入测试活动名", value='', interactive=True)
    
    # 组件 - 操作 - 触发函数 - 输入 - 输出
    option.select(on_select_option, None, [input_options, inputs])

    def on_select_input_options(evt: gr.SelectData):
        '''
        加载之前创建的测试活动的描述
        '''
        if evt.value:
            inputs = evt.value
            llm = get_llm_by_inputs(inputs)
            details = llm.get_writer('td').get_input_context()
            if not config.get('llm'):
                config['llm'] = llm
            return gr.Textbox(interactive=False), gr.Textbox(details), gr.Info(f"加载测试项目成功")

    input_options.select(on_select_input_options, None, [inputs, details])
    
    def on_submit_create(inputs, details):
        '''
        新建测试活动
        params:
            inputs[str]:创建的测试活动名
        '''
        if not inputs:
            gr.Info("请输入测试活动名")
            return
        exists_options = get_available_input_options()
        if inputs in exists_options:
            gr.Info(f"测试活动名：{inputs}已经存在，请重新输入")
            return
        llm = get_llm_by_inputs(inputs)
        llm.get_writer('td').init_by_details(details)
        llm.save('td')
        config['llm'] = llm
        gr.Info(f"创建测试活动：{inputs}成功，接下来输入需求文档构建向量数据库")
        
    submit_create.click(on_submit_create, [inputs, details], None)

    def on_submit_start(input_options,files):
        '''
        选择加载测试活动名，或修改TdWriter对象中的配置，并保存
        params:
            input_options[str]:选择要加载的测试活动
        '''
        if not input_options:
            gr.Info("请选择测试活动")
            return
        target_directory  = f"../knowledge_db/{input_options}"
        persist_path = f"../vector_db/chroma/{input_options}"
        embedding = config.get("embedding")
        embedding_key = config.get("embedding_key")
        generate_files(target_directory, files)
        # 更新向量数据库
        get_vectordb(target_directory, persist_path, embedding, embedding_key)
        gr.Info(f"已经上传文档成功，接下来继续上传文件，或下一步去创建缺陷知识库吧")
        
    def generate_files(target_directory, files):
        import shutil
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        for source_file in files:
            shutil.copy2(source_file, target_directory)

    submit_start.click(on_submit_start, [input_options,files], None)

    def get_llm_by_inputs(inputs):
        '''
        根据输入的测试活动名，获得Pipeline_Wrapper对象，去调用tdWriter对象
        如果测试活动对应的tdWriter对象不存在，就进行初始化，这里会直接初始化全部Writer子类
        如果存在，就返回之前保存的对象
        '''
        output_path = f"../chathistory/{inputs}"
        file_path  = f"../knowledge_db/{inputs}"
        persist_path = f"../vector_db/chroma/{inputs}"
        config["file_path"] =  file_path
        config["persist_path"] =  persist_path
        llm = Pipeline_Wrapper(output_path, config)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            llm.init()
            return llm
        else:
            llm.load_checkpoints()
            return llm