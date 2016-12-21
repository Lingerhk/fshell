# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-11
# desc: sRetv base


from fss_cfg import *
from fss_net import *

class FsContentProto:

    @staticmethod
    def check_valid(reqJson):
        def _check_valid(reqJson):
            if not reqJson.has_key("task_id"):
                return False, "task_id is not exist!"
                                        
            if not reqJson.has_key("dev_name"):
                return False, "dev_name is not exist!"

            if not reqJson.has_key("agent_id"):
                return False, "agent_id is not exist"
                                                                                        
            if not reqJson.has_key("msg_protocol"):
                return False, "msg_protocol is not exist!"
                                                                                                                       
            if not reqJson.has_key("msg_type"):
                return False, "msg_type is not exist!"
        
            if not reqJson.has_key("data"):
                return False, "data is not exist!"

            return True, ""

        bRet, sRet = _check_valid(reqJson)
        if not bRet:
            Log.err("reqJson: %s not valid(%s)" %(reqJson, sRet))
        return bRet
    
    
    @staticmethod
    def response_packet(session, reqJson, rspProto, rspType, rspData):
        rspJson = {}
        rspJson['task_id'] = reqJson['task_id']
        rspJson['dev_name'] = reqJson['dev_name']
        rspJson['agent_id'] = reqJson['agent_id']
        rspJson['msg_protocol'] = rspProto
        rspJson['msg_type'] = rspType
        rspJson['data'] = rspData
        rspStr = json.dumps(rspJson)        
        g_fsNet.send_req(session, rspStr)
        
        return True, ""
