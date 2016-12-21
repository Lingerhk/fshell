# -*- coding: UTF-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-11
# desc: srv manager



from fss_cfg import *
from fss_net import *
from fss_srv_base import *
from fss_proto_type import *

#from fs_report_info_dao import *


class FsManagerSrv:
    
    def __init__(self):
        self.ip      =   SERVER_IP
        self.port    =   SERVER_PORT
        self.mode    =   FsNetMode.T_SYN_MODE
        
    
    def deal_pkg(self, session, reqJson):
        
        bRet = FsContentProto.check_valid(reqJson)
        if not bRet:  return False, ""
        
        # 记录心跳
        """
        HpsReportInfoDao.insert_node(
            reqJson['task_id'], 
            reqJson['dev_name'],
            reqJson['plugin_id'],
            reqJson['msg_protocol'],
            reqJson['msg_type'],
            reqJson['data'])
        """

        proto = reqJson['msg_type']
        rspProto = ""
        rspData = ""
       
        """
        if proto == HpProtoTypeEnum.T_HPC_ROUTE_SYN_IP_REQ:
            rspProto = HpProtoTypeEnum.T_HPC_ROUTE_SYN_IP_REQ
            rspJson = {
                'route_syn_ip' : ROUTE_SYN_IP,
                'route_syn_port' : ROUTE_SYN_PORT
            }
            
            rspData = json.dumps(rspJson)
        
        elif proto == HpProtoTypeEnum.T_HPC_ROUTE_ASY_IP_REQ:
            rspProto = HpProtoTypeEnum.T_HPC_ROUTE_ASY_IP_REQ
            rspJson = {
                'route_asy_ip' : ROUTE_ASY_IP,
                'route_asy_port' : ROUTE_ASY_PORT
            }
            
            rspData = json.dumps(rspJson)
            
        else:
            Log.err("proto: %d not valid!" %(proto))
            rspProto = HpProtoTypeEnum.T_HP_ERR
            rspData = ""   
        """


        return FsContentProto.response_packet(session, reqJson, FsProtoProtoEnum.T_HP_CMD_RSP, rspProto, rspData)
