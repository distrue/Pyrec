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
        dump = file_parse(path, [], file_type)
        if(dump):
            logger.info(path)
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
    parse_type = {}
    parse_type['pyrec'] = ('# s_script', '# e_script')
    parse_type['py'] = ('# s_script', '# e_script')
    parse_type['js'] = ('// s_script', '// e_script')
    if(file_type not in parse_type):
        return d_dict
    else:
        anno = parse_type[file_type]

    with OpenFile() as f:
        f.open(path, 'r')
        # TODO : data parse 오토마타 구성
        while(not f.EOF):
            f.readuntil(anno[0])
            if(f.EOF):
                break
            dump = f.readuntil(anno[1])
            ndump = dump.split('\n')[0]
            d_dict.append({'title': ndump, 'data': ''.join(dump.split(ndump)[1:])})
            if(f.EOF):
                # e_script 종료 제대로 되지 않은 상태
                pass
    return d_dict
