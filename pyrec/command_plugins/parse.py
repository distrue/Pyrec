import os
from pyrec.fileio import OpenFile

def lookup_dir(path, ignore):
    ret = {}
    if(os.path.isdir(path)):
        ret['type'] = 'dir'
        for i in os.listdir(path):
            if(i in ignore):
                continue
            now_path = os.path.join(path, i)
            dump = lookup_dir(now_path, ignore)
            ret[i] = dump    
    else:
        ret['type'] = 'file'
        ret['location'] = path
        ret = file_parse(path, ret, file_type)
    return ret


def file_parse(path, d_dict, file_type):
    anno = ()
    if(file_type == 'pyrec'):
        anno = ('# s_script', '# e_script')
    elif(file_type == 'py'):
        anno = ('# s_script', '# e_script')
    with OpenFile() as f:
        f.open(path, 'r')
        while(not self.EOF):
            f.readuntil(anno[0])
            if(self.EOF):
                break
            dump = f.readuntil(anno[1])
            dump = dump.split('\n')
            d_dict['script'].append({'title': dump[0], 'data': dump[1]})
            if(self.EOF):
                # e_script 종료 제대로 되지 않음, error!
                pass
    return d_dict
