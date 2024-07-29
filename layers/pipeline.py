import os

from layers.td_writer import TdWriter
from layers.tp_writer import TpWriter
from layers.case_writer import CaseWriter

class Pipeline:
    def __init__(self, model, file_path, persist_path,
                 api_key, wenxin_secret_key,
                 embedding,embedding_key) -> None:
        self.model = model
        self.file_path = file_path
        self.persist_path = persist_path
        self.api_key = api_key
        self.wenxin_secret_key = wenxin_secret_key
        self.embedding = embedding
        self.embedding_key = embedding_key
        self.init_layers()

    def init_layers(self):
        self.td_writer = self.get_td_writer()
        self.tp_writer = self.get_tp_writer(self.td_writer)
        self.case_writer = self.get_case_writer(self.td_writer, self.tp_writer)
    
    def get_td_writer(self):
        td_writer = TdWriter(
            output_path=os.path.join(self.output_path, 'td_writer'),
            model=self.model
        )
        return td_writer
    
    def get_tp_writer(self, td):
        tp_writer = TpWriter(
            output_path=os.path.join(self.output_path, 'tp_writer'),
            model=self.model
        )
        tp_writer.init_by_td_writer(td)
        return tp_writer
    
    def get_case_writer(self, td, tp):
        case_writer = CaseWriter(
            output_path=os.path.join(self.output_path, 'case_writer'),
            model=self.model,
        )
        case_writer.init_by_td_and_tp_writer(td, tp)
        return case_writer