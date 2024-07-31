import os

from layers.td_writer import TdWriter
from layers.tp_writer import TpWriter
from layers.case_writer import CaseWriter

class Pipeline:
    def __init__(self, output_path, config) -> None:
        self.output_path = output_path
        self.config = config
        self.init_layers()

    def init_layers(self):
        """
        初始化顺序
        1. TdWriter: 创建缺陷知识库
        2. TpWriter：创建测试因子和测试用例标题
        3. CaseWriter：创建测试用例+具体步骤
        """
        self.td_writer = self.get_td_writer()
        self.tp_writer = self.get_tp_writer(self.td_writer)
        self.case_writer = self.get_case_writer(self.td_writer, self.tp_writer)
    
    def get_writer(self, layer_name):
        if layer_name == 'td':
            return self.td_writer
        elif layer_name == 'tp':
            return self.tp_writer
        elif layer_name == 'case':
            return self.case_writer
        else:
            raise ValueError(f"layer:{layer_name} 不存在!")

    def get_td_writer(self):
        td_writer = TdWriter(
            output_path=os.path.join(self.output_path, 'td_writer'),
            config = self.config
        )
        return td_writer
    
    def get_tp_writer(self, td):
        tp_writer = TpWriter(
            output_path=os.path.join(self.output_path, 'tp_writer'),
            config = self.config
        )
        tp_writer.init_by_td_writer(td)
        return tp_writer
    
    def get_case_writer(self, td, tp):
        case_writer = CaseWriter(
            output_path=os.path.join(self.output_path, 'case_writer'),
            config = self.config,
        )
        case_writer.init_by_td_and_tp_writer(td, tp)
        return case_writer