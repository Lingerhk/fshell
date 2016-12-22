# -*- coding: UTF-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-21
# desc: detection web_log




import time

class FsaTaskWeblog:

    def __init__(self):
        pass






    def _read_content(self, filename=""):
        file_seek = self.read_seek(filename)
        f = open(filename, "r")
        f.seek(file_seek)
        while True:
            _row = f.readline()
            file_seek += len(_row)
            self.write_seek(filename, file_seek)
            
            try:
                # here get web_log content ...
                req_time = ""
                req_data = ""
                req_method = ""
                req_uri = ""
                req_referer = ""

            except:
                pass
            if not _row: break
        f.close()



    @staticmethod
    def start_task(self):
        while True:
            self.read_log_file()
            if self.read_time_log() == 0:
                pass
            break

        
