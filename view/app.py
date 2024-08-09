import gradio as gr

import os
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from view.tab_main_page import tab_main_page
from view.tab_td_page import tab_td_page
from view.tab_vectordb_page import tab_vectordb_page

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
        
    config = {
        'llm': None,
        'model':"ERNIE-Speed-128K",  # 使用的模型名称
        'temperature':0.1,  # 控制生成的随机性
        'top_k':5,  # 返回检索的前k个相似文档
        'api_key':"clLcz3pG0KETHqhDkFUURfSn",  # API密钥
        'wenxin_secret_key':"kjmDsDF73j5LnCW2LADz2EIOreYHtaGS",  # 文心秘钥
        'embedding':"qianfan",  # 使用的嵌入模型
        "embedding_key" : {
            "qianfan_ak":"clLcz3pG0KETHqhDkFUURfSn",
            "qianfan_sk":"kjmDsDF73j5LnCW2LADz2EIOreYHtaGS",
        }
    }
    tab_main_page(config)
    tab_td_page(config)
    tab_vectordb_page(config)

if __name__ == "__main__":
    demo.queue()
    demo.launch(share=False, inbrowser=True)
