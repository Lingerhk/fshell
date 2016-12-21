# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-12
# desc: fshell agent main


import os
import sys
sys.path.append("..")
sys.path.append("../base")
sys.path.append("../bean")

from fsa_task import *
from fsa_task_type import *
from det_web_log import *
from det_statis_tics import *
from det_file_att import *
from det_dan_func import *
from det_fuzz_hash import *


class FsaMain:
    
    def __init__(self):
        
        self.taskPid = 0
        self.task = None
     
    
    def _task_run(self, taskType):        
        
        if taskType == FsaTaskType.F_WEBLOG:
            taskWeblog = FsaTaskWeblog()
            taskWeblogTid = threading.Thread(target = taskWeblog.start_task)
            taskWeblogTid.start()

        elif taskType == FsaTaskType.F_STATICS:
            taskStatics = FsaTaskStatics()
            taskStaticsTid = threading.Thread(target = taskStatics.start_task)
            taskStaticsTid.start()

        elif taskType == FsaTaskType.F_FILEATT:
            taskFileatt = FsaTaskFileatt()
            taskFileattTid = threading.Thread(target = taskFileatt.start_task)
            taskFileattTid.start()

        elif taskType == FsaTaskType.F_DANFUNC:
            taskDanfunc = FsaTaskDanfunc()
            taskDanfuncTid = threading.Thread(target = taskDanfunc.start_task)
            taskDanfuncTid.start()

        elif taskType == FsaTaskType.F_FUZZHASH:
            taskFuzzhash = FsaTaskFuzzhash()
            taskFuzzhashTid = threading.Thread(target = taskFuzzhash.start_task)
            taskFuzzhashTid.start()

        else:
            return False

        return True

        
    def _task_start(self, taskType):
        self.taskType = taskType
        
        pid = os.fork()
        if pid == -1: 
            Log.err("os.fork err!")
            return False
        
        if pid == 0:
            retCode = 0
            try:
                bRun = self._task_run(taskType)
                if not bRun: retCode = -1
            except Exception, e:
                Log.err("taskType: %s, err: %s" %(str(taskType), str(traceback.format_exc())))
                retCode = -1
                
            if retCode == -1:
                FsaTaskClient.report_task(self.taskType, FsaTaskStatus.T_FAIL, "task_exec ERR!")
            else:
                FsaTaskClient.report_task(self.taskType, FsaTaskStatus.T_FINISH, "sdsd")
            
            os._exit(retCode)
            
        self.taskPid = pid
        return True
    
      
    def _task_check(self):   
        if not self.taskPid:  return False
        
        try:
            os.waitpid(self.taskPid, os.WNOHANG)
        except Exception, e:
            self.taskPid = 0
            return False
        
        return True
    
        
    def run(self):
        count = 0
        while True:
            
            if self.taskPid > 0:
                if self._task_check() == False:
                    count += 1

            else:
                bRet, taskType = FsaTaskClient.get_task()
                if bRet:
                    if taskType != None:
                        try:
                            bRet = self._task_start(taskType)
                            if not bRet:
                                Log.err("task_start(%s) ERR" %(str(taskType)))
                                FsaTaskClient.report_task(taskType, FsaTaskStatus.T_FAIL, "task_start Fail!")

                        except Exception, e:
                            Log.err("taskType: %s, %s" %(taskType, traceback.format_exc()))
                            FsaTaskClient.report_task(taskType, FsaTaskStatus.T_FAIL, "task_start Fail!")
                
            time.sleep(3)



if __name__ == "__main__":
    
    def main():
        fsaMain = FsaMain()
        fsaMain.run()
        
    main()

