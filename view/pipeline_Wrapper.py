import os
import json
from view.pipeline import Pipeline
from common.untils import json_load, json_dumps

'''
作为中间层
1. 负责获取每个writer对象给view对象调用
2. 将view对象输入的数据，传递给writer对象后保存记录
'''
class Pipeline_Wrapper(Pipeline):
    def __init__(self, output_path, config) -> None:
        super().__init__(output_path, config)

        # 记录每个环节的被调用轮次
        self.layers = {
            'td': {'curr_checkpoint_i': -1},
            'tp': {'curr_checkpoint_i': -1},
            'case': {'curr_checkpoint_i': -1}
        }

    def init(self):
        '''
        初始化测试活动
        '''
        for layer_name in self.layers.keys():
            self.save(layer_name)
        self.save_checkpoints()
    
    def save(self, layer_name):
        '''
        记录每个环节被调用的入参
        params：
            layer_name：期望调用哪个writer对象
        '''
        layer, writer = self.get_layer_config(layer_name), self.get_writer(layer_name)
        cur_checkpoint_i = layer['curr_checkpoint_i'] + 1
        checkpoint_path = os.path.join(writer.output_path, ".checkpoints", f"checkpoint_{cur_checkpoint_i}")
        os.makedirs(checkpoint_path, exist_ok=True)
        writer.save(checkpoint_path)
        layer['curr_checkpoint_i'] = cur_checkpoint_i
        self.save_checkpoints()
    
    def save_checkpoints(self):
        '''
        保存调用轮次
        app.json:
        '''
        filename = os.path.join(self.output_path, "app.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.layers, f, ensure_ascii=False, indent=4)
    
    def load_checkpoints(self):
        '''
        加载最新一轮的调用记录
        '''
        filename = os.path.join(self.output_path, "app.json")
        with open(filename, 'r', encoding='utf-8') as f:
            self.layers = json.load(f)
        
        for layer_name, layer in self.layers.items():
            writer = self.get_writer(layer_name)
            curr_checkpoint = f"checkpoint_{layer['curr_checkpoint_i']}"
            writer.load(os.path.join(writer.output_path, ".checkpoints", curr_checkpoint))
    
    def get_layer_config(self, layer_name = None):
        layer_config = self.layers.get(layer_name)
        return layer_config
    
    def get_writer(self, layer_name):
        '''
        根据输入的layer_name返回不同的writer对象
        '''
        writer = super().get_writer(layer_name)
        return writer