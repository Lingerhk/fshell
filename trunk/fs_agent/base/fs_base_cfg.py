# -*- coding: utf-8 -*-

# project: fshell 
# author: s0nnet
# time: 2016-12-10
# desc: agent base conf

'''
LOG_LEVEL
    DEBUG   =   1
    INFO    =   2
    WARINING =  3
    ERR     =   4
    ALERT   =   5
    CLOSE   =   10
'''


import os
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

import ConfigParser


class AgentConf:
    
    def __init__(self):
        cfgFile = path + '/../conf/fshell_agent.conf'
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(cfgFile)


    def get_base_conf(self, option):
        try:
            return self.conf.get("BASE", option)
        except:
            return None


    def get_weblog_conf(self, option):
        try:
            return self.conf.get("WEBLOG", option)
        except:
            return None


    def get_statics_conf(option):
        try:
            return self.conf.get("STATICS", option)
        except:
            return None


    def get_fileatt_conf(option):
        try:
            return self.conf.get("FILEATT", option)
        except:
            return None


    def get_danfunc_conf(option):
        try:
            return self.conf.get("DANFUNC", option)
        except:
            return None


    def get_fuzzhash_conf(option):
        try:
            return self.conf.get("FUZZHASH", option)
        except:
            return None



class BaseConf:

    conf = AgentConf()

    LOG_LEVEL       =   int(conf.get_base_conf("log_level"))
    LOG_DIR         =   conf.get_base_conf("log_dir")
    LOG_PREFIX      =   conf.get_base_conf("prefix")
    IS_CTR_LOG      =   bool(conf.get_base_conf("is_ctr_log"))

    SERVER_IP       =   conf.get_base_conf("server_ip")
    SERVER_PORT     =   int(conf.get_base_conf("server_port"))



if __name__ == "__main__":

    print BaseConf.SERVER_IP




