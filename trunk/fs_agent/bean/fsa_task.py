# -*- coding: utf-8 -*-

# project: fshll
# author: s0nnet
# time: 2016-12-12
# desc: 任务接收/上报模块

import sys
import uuid


sys.path.append("../base")
sys.path.append("../net")
from fsa_net import *



class FsaTaskStatus:
    
    T_RUN       =  "run"
    T_FAIL      =   "fail"
    T_FINISH    =   "finish"
    
    statusList = [T_RUN, T_FAIL, T_FINISH]
    
    @staticmethod
    def valid_check(status):
        for st in FsaTaskStatus.statusList:
            if st == status: 
                return True
        
        return False

    

class FsaTaskClient:

    @staticmethod
    def _send_pkt(taskData):
        reqJson = {}
        reqJson['task_id'] = uuid.uuid1().get_hex()
        reqJson['dev_name'] = 'test'
        reqJson['agent_id'] = 1234
        reqJson['msg_protocol'] = 3
        reqJson['msg_type'] = 22
        reqJson['data'] = taskData

        return FsaNet.send_req(reqJson)

    
    @staticmethod
    def get_task():

        # read from local conf file


        bRet = True
        taskType = "web_log"

        return bRet, taskType
    
    
    @staticmethod
    def report_task(taskType, taskStatus, taskData):
        if FsaTaskStatus.valid_check(taskStatus) == False:
            Log.err("status(%d) is not valid" %(taskStatus))
            return False, "status(%d) is not valid" %(taskStatus)
        
        if taskData == None: taskData = taskStatus
        
        # 预留　结果本地缓存模块
        #
        #
        #
        #
        #

        return MssTaskClient._send_pkt(taskData)


if __name__ == "__main__":
    
    bRet, taskType = FsaTaskClient.get_task()
    
    print bRet, taskType
    
    print FsaTaskClient.report_task("web_log", FsaTaskStatus.T_RUN, "askef xx")
        
