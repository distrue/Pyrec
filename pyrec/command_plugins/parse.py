import os
from pyrec.fileio import OpenFile
import logging
logger = logging.getLogger(__name__)


def lookup_dir(record_path, path, ignore):
    if(os.path.isdir(path)):
        for i in os.listdir(path):
            if(i in ignore):
                continue
            now_path = os.path.join(path, i)
            lookup_dir(record_path, now_path, ignore)
    else:
        file_type = path.split(os.sep)[-1]
        file_type = file_type.split('.')[-1]
        logger.info(path)
        dump = file_parse(path, [], file_type)
        for iname in dump:
            # script.json 처리
            ipath = os.path.join(record_path, iname['title'])
            cou = 1
            while(os.path.exists(ipath)):
                ipath = os.path.join(record_path, iname['title'] + '.' + str(cou))
                cou += 1
            with OpenFile() as f:
                f.open(ipath, 'w')
                f.write(iname['data'], 'text/plain')
            # TODO : keyword.json 처리


def file_parse(path, d_dict, file_type):
    anno = ()
    if(file_type == 'pyrec'):
        anno = ('# s_script', '# e_script')
    elif(file_type == 'py'):
        anno = ('# s_script', '# e_script')
    else:
        return d_dict
    with OpenFile() as f:
        f.open(path, 'r')
        while(not f.EOF):
            f.readuntil(anno[0])
            if(f.EOF):
                break
            dump = f.readuntil(anno[1])
            ndump = dump.split('\n')[0]
            d_dict.append({'title': ndump, 'data': dump.split(ndump)[1]})
            if(f.EOF):
                # TODO : e_script 종료 제대로 되지 않음, error!
                pass
    return d_dict
