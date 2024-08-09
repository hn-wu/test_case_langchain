from layers.writer import Writer

class VectordbWriter(Writer):

    def __init__(self, output_path, config):
        super().__init__(output_path, config)
        self.vectordb_content = {}
        self.load()
        system_prompt = f'获取知识库信息'
        out_prompt = ""
        self.update_system_prompt(system_prompt, out_prompt)
    
    def init_by_vectordb_writer(self, vectordb_writer):
        self.vectordb_writer = vectordb_writer
    
    def get_input_context(self):
        pass

    def set_output(self, td_content):
        pass
    
    def get_attrs_needed_to_save(self):
        pass