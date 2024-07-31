import gradio as gr

import os
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from view.tab_main_page import tab_main_page

info = \
"""
1. 新建测试项目，上传需求文档
2. 输入Story，生成Story的缺陷知识库，产出测试因子
3. 根据测试因子生成测试用例标题
4. 根据测试用例标题和测试因子生成完整的测试用例，包含测试步骤
"""

with gr.Blocks() as demo:
    gr.Markdown("# Test-Case-Langchain 1.0")
    with gr.Accordion("使用指南"):
        gr.Markdown(info)
    config = {'llm': None, 'chat_context_limit': 2000, 'auto_compress_context': True}
    tab_main_page(config)

if __name__ == "__main__":
    demo.queue()
    demo.launch(share=False, inbrowser=True)
