from test_case.history_chain_self import Client as HistoryChat

class Writer:
    def __init__(self, system_prompt, output_path, model, sub_model):
        self.output_path = output_path

        self.config = {'chat_context_limit': 2000, 'auto_compress_context': True, }
        
        self.system_prompt = system_prompt
        self.set_model(model, sub_model)

        self.chat_history = {
            'system_messages': [{'role':'system', 'content': system_prompt}],
            }