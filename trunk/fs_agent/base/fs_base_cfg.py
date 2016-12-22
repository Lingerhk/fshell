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
path = os.path.dirname(os.path.realpath(__ifle__))
os.chdir(path)

import ConfigParser


class AgentConf:
    
    def __init__(self):
        self.cfgFile = path + '/../conf/fshell_agent.conf'
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.cfgFile)


    @staticmethod
    def get_base_conf(self, option):
        try:
            return self.conf.get("BASE", option)
        except:
            return None


    @staticmethod
    def get_weblog_conf(self, option):
        try:
            return self.conf.get("WEBLOG", option)
        except:
            return None


    @staticmethod
    def get_statics_conf(self, option):
        try:
            return self.conf.get("STATICS", option)
        except:
            return None


    @staticmethod
    def get_fileatt_conf(self, option):
        try:
            return self.conf.get("FILEATT", option)
        except:
            return None


    @staticmethod
    def get_danfunc_conf(self, option):
        try:
            return self.conf.get("DANFUNC", option)
        except:
            return None


    @staticmethod
    def get_fuzzhash_conf(self, option):
        try:
            return self.conf.get("FUZZHASH", option)
        except:
            return None



class BaseConf:


    LOG_LEVEL       =   int(AgentConf.get_base_conf("log_level"))
    LOG_DIR         =   AgentConf.get_base_conf("log_dir")
    LOG_PREFIX      =   AgentConf.get_base_conf("prefix")
    IS_CTR_LOG      =   bool(AgentConf.get_base_conf("is_ctr_log"))

    SERVER_IP       =   AgentConf.get_base_conf("server_ip")
    SERVER_PORT     =   int(AgentConf.get_base_conf("server_port"))








