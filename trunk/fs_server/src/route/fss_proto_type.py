# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-11
# desc: 通信协议定义


class FsProtoProtoEnum:
    T_HP_EVIL_UP     = 0x01
    T_HP_STAT_REPORT = 0x02
    T_HP_CMD_REQ     = 0x03
    T_HP_CMD_RSP     = 0x04


class FsProtoTypeEnum:
    # 获取配置
    T_HPC_ROUTE_SYN_IP_REQ      =   0x01
    T_HPC_ROUTE_ASY_IP_REQ      =   0x02
    T_HPC_GET_PLUGIN_ALL_CONF   =   0x03
    
    # 服务端命令下发(0x-60 ~ 0xa0)
    T_HPC_PLUGIN_NEW    =   0x60
    T_HPC_PLUGIN_START  =   0x61
    T_HPC_PLUGIN_STOP   =   0x62
    T_HPC_PROXY_RULE_UPDATE = 0x63
    T_HPC_PLUGIN_ADD_IP = 0x64
    T_HPC_PLUGIN_DESTROY = 0x65
    T_HPC_PLUGIN_DEL_IP = 0x66
    T_HPC_CLIENT_RESET = 0x67
    
    # 心跳和错误上报
    T_HPC_HEART_BEAT    =   0xa0
    T_HPC_CLIENT_REPORT =   0xa1          
    T_HPC_PLUGIN_REPORT =   0xa2
    T_HPC_KVM_ERR       =   0xa3
    T_HP_ERR            =   0xff

