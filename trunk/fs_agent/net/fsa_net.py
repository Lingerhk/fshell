# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-09
# desc: Agent 网络数据包发送

import sys
sys.path.append('../net')
sys.path.append("../base")

from fs_log import *
from fs_base_cfg import *
from fsa_nethead import *


'''
  跟进参数封装成相应，发给route_srv
'''
class FsaNet:
    
    @staticmethod
    def _recv_packet(sock):
        sock.settimeout(60)
        
        try:
            buf = sock.recv(16 * 1024)
            if buf == None or len(buf) == 0:  
                Log.err("sock.recv ERR!")
                return False, "client close connection"
            
            if len(buf) < NetHead.size(): return False, "recv info error!"
            
            netHead = NetHead.decode(buf)
            if netHead == None:
                return False, "NetHead.decode ERR"
                
            pkgLen = netHead.pkgLen
            while len(buf) < pkgLen:
                sock.settimeout(3)
                val = sock.recv(16 * 1024)
                sock.settimeout(None)
                if val == None or len(val) == 0:
                    Log.err("sock.recv ERR!")
                    return False, "client close connection"
                
                buf = buf + val
            
            return True, buf[NetHead.size() : ]
        
        except Exception, e:
            Log.err(traceback.format_exc())
            return False, str(e)
    
    
    @staticmethod
    def _send_str_conn(sendStr):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            code = sock.connect_ex((SERVER_IP, SERVER_PORT))
            if code != 0:
                Log.err("sock.connect(%s, %d) ERR(%d)" % (SERVER_IP, SERVER_PORT, code)) 
                sock.close()
                return False, "connect to route_srv Fail!"
            
            print "send_to_route", len(sendStr)
            sock.sendall(sendStr)
            bRet, sRet = FsaNet._recv_packet(sock)
            Log.info("send_cmd: %s, recv_pack: %s" %(sendStr, sRet))
            sock.close()
            return bRet, sRet
            
        
        except Exception, e:
            Log.err("sock.connect(%s, %d) ERR(%s)" %(SERVER_IP, SERVER_PORT, str(e)))
            if sock != None: sock.close()
            return False, str(e)
            
            
    @staticmethod
    def _send_str(reqStr):

        netHead = NetHead()
        netHead.start = NetHead.START_CODE
        netHead.type = 0
        netHead.pkgLen = len(reqStr) + NetHead.size()
        headStr = NetHead.encode(netHead) 
        sendStr = headStr + reqStr
        
        return FsaNet._send_str_conn(sendStr)

    
    @staticmethod
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


    # 发给srv route
    @staticmethod
    def send_req(reqJson):
        
        def _get_rsp_info(rspCnt):
            try:
                rspJson = json.loads(sRet)
                if rspJson['data'].find("code") == -1:
                    Log.err("cmd_rsp: %s is not valid!" %(rspJson['data']))
                    return False, rspJson['data']
                rspDataJson = json.loads(rspJson['data'])
                
                if not rspDataJson.has_key('code'):
                    return False, rspJson['data']
                if not rspDataJson.has_key('val'):
                    return False, rspJson['data']
                
                code = rspDataJson['code']
                val = rspDataJson['val']
                
                if code == 0:  return True, val
                return False, val
            
            except Exception, e:
                Log.err(traceback.format_exc())
                return False, rspCnt
                
            
        bRet, sRet = FsaNet._check_valid(reqJson)
        if not bRet:
            Log.err("%s %s" %(str(reqJson), sRet))
            return bRet, sRet
        
        reqStr = json.dumps(reqJson)
        Log.debug(reqStr)
        bRet, sRet = FsaNet._send_str(reqStr)
        if bRet:
            return _get_rsp_info(sRet)
            
        return bRet, sRet
    



if __name__ == "__main__":

    def test_send_data(data):
        reqJson = {}
        reqJson['task_id'] = '123ver234cv234'
        reqJson['dev_name'] = 'xy_01'
        reqJson['agent_id'] = 12345
        reqJson['msg_protocol'] = 0x03
        reqJson['msg_type'] = 0x64
        reqJson['data'] = data

        return FsaNet.send_req(reqJson)
    
    test_send_data("heheda")
