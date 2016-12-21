# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: base conf


import os
import sys

'''
LOG_LEVEL
    DEBUG   =   1
    INFO    =   2
    WARINING =  3
    ERR     =   4
    ALERT   =   5
    CLOSE   =   10
'''
class BaseConf:

    LOG_LEVEL       =   2
    LOG_DIR         =   "../../log/"
    LOG_PREFIX      =   ""
    IS_CTR_LOG      =   True

    SQL_HOST        =   "222.24.XX.XX"
    SQL_PORT        =   3306
    SQL_USER        =   "root"
    SQL_PASSWD      =   "rtxxxx"
    SQL_DB          =   "fshell"
