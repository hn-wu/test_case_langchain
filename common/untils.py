import json

def json_load(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def json_dumps(json_object):
    return json.dumps(json_object, ensure_ascii=False, indent=1)

def json_save(json_object, output_file):
    '''
    以文件的形式保存当前调用writer的入参
    params
        json_object：
        output_file：要保存的文件名
    '''
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_dumps(json_object))