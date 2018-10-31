import os


def top_path(OS_type):
    path = ''
    if(OS_type == 'windows'):
        path = os.path.abspath(__file__).split(os.sep)[0] + os.sep  # window의 경우 root의 위에 존재하는 drive의 값을 가져온다.
    # TODO : linux 환경 check
    return path


# Openfile을 통해서 file을 open하면 객체의 open, close를 자동으로 수행함.
# 같은 object로 다른 file을 open하면 기존의 file open은 자동 close
# open하는 file이 존재하지 않으면 생성, 디렉토리 또한 생성
class OpenFile():
    def __enter__(self):
        self.fd = None
        self.file_path = ''
        return self  # self를 return 해줘야 with~as구문에서 object를 받을 수 있다.

    def __exit__(self, type, value, traceback):
        if(not self.fd or self.fd == None):  # TODO : None check! None can't be filtered by not phrase
            return
        self.fd.close()

    def open(self, file_abspath, open_type):
        if(self.fd and str(type(self.fd)) == "<class \'_io.TextIOWrapper\'>"):  # if fd is already opening other file
            self.fd.close()
        self.open_type = open_type
        self.file_path = file_abspath
        if(not os.path.isdir(os.path.dirname(self.file_path))):
            print(os.path.isdir(os.path.dirname(self.file_path)), os.path.dirname(self.file_path), self.file_path)
            os.makedirs(os.path.dirname(self.file_path))
        if(not os.path.exists(self.file_path)):
            f = open(self.file_path, 'w')
            f.write('')
            f.close()
        self.fd = open(self.file_path, self.open_type)

    def read(self, data_type):
        if(self.open_type != 'r' and self.open_type != 'rb'):
            print('File is not opened with read mode')  # TODO : log로 전환
            return
        if(not data_type):  # TODO : data_type **arg로 전환
            data_type = 'text/plain'
        # TODO : encoding type 지정

        dump = self.fd.read()
        if(data_type == 'application/json'):
            import json
            dump = json.loads(dump)

        return dump

    # TODO : readuntil 함수

    def write(self, dump, data_type):
        if(self.open_type != 'w' and self.open_type != 'wb'):
            print('File is not opened with write mode')  # TODO : Log로 전환
            return
        if(not data_type):  # TODO : data_type **arg로 전환
            data_type = 'text/plain'
        # TODO : encoding type 지정

        if(data_type == 'json'):
            import json
            dump = json.dumps(dump)
        self.fd.write(dump)

        return 'Write success'
