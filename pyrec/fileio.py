import os
import logging
import json
logger = logging.getLogger(__name__)


def top_path(OS_type):
    path = os.path.abspath(__file__).split(os.sep)[0] + os.sep
    return path


# Openfile을 통해서 file을 open하면 객체의 open, close를 자동으로 수행함.
# 같은 object로 다른 file을 open하면 기존의 file open은 자동 close
# open하는 file이 존재하지 않으면 생성, 디렉토리 또한 생성
class OpenFile():
    def __enter__(self):
        self.fd = None
        self.file_path = ''
        self.EOF = False
        return self  # self를 return 해줘야 with~as구문에서 object를 받을 수 있다.

    def __exit__(self, type, value, traceback):
        if(not self.fd or self.fd == None):  # TODO : None check! None can't be filtered by not phrase
            return
        self.fd.close()

    def open(self, file_abspath, open_type='w'):
        if(self.fd and str(type(self.fd)) == "<class \'_io.TextIOWrapper\'>"):  # if fd is already opening other file
            self.fd.close()
        self.open_type = open_type
        self.file_path = file_abspath
        if(not os.path.isdir(os.path.dirname(self.file_path))):
            os.makedirs(os.path.dirname(self.file_path))
        if(not os.path.exists(self.file_path)):
            f = open(self.file_path, 'w')
            f.write('')
            f.close()
        if(self.open_type == 'rb' or self.open_type == 'wb'):
            # does not support encoding
            self.fd = open(self.file_path, self.open_type)
        else:
            self.fd = open(self.file_path, self.open_type, encoding='utf-8')

    def read(self, data_type='text/plain'):
        if(self.open_type == 'r'):
            dump = self.fd.read()
            # s_script \xa0 non-breaking space encode error python
            # \xa0 처리 (non-breaking space)
            dump.replace(u'\xa0', '')
            # e_script
            if(data_type == 'text/plain'):
                pass
            elif(data_type == 'application/json'):
                import json
                dump = json.loads(dump)
            else:
                logger.info('unknown open type; opened by text/plain')

        else:
            logger.error('File is not opened with read mode')
            return

        return dump

    def readuntil (self, ustr):
        if(self.open_type != 'r'):
            logger.error('only available in open_type')
            raise Exception
        if (len(ustr) == 0):
            return ""
        nmi = 0  # current non-matching index
        out = ""
        while (True):
            c = self.fd.read(1)
            # TODO : 한글 data 처리
            if (c == ""):
                self.EOF = True
                return out
            out += c
            if (c == ustr[nmi]):
                nmi += 1
                if (nmi > len(ustr)-1):
                    return out[:(-1)*len(ustr)]
            else:
                nmi = 0
        return out


    def write(self, dump, data_type='text/plain'):
        if(self.open_type == 'w'):
            if(data_type == 'text/plain' and self.open_type == 'w'):
                self.fd.write(dump)
            if(data_type == 'application/json' and self.open_type == 'w'):
                dump = json.dumps(dump)
                self.fd.write(dump)

        else:
            logger.info('File is not opened with available write mode(\'w\')')
            return

        return 'Write success'
