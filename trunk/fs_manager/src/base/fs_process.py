# -*- coding: UTF-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: 进程创建封装


from subprocess import *
from fs_log import *


def bs_system(cmd, stdout = False, stderr = True):
    bRet = False
    
    if not stderr:      cmd = "%s >> /dev/null 2>&1" %(cmd)
    elif not stdout:    cmd = "%s >> /dev/null" %(cmd)
    
    try:
        retState = os.system(cmd)
    except Exception, e:
        Log.err("cmd(%s) ERR(%s)" %(cmd, str(e)))
        retState = -1
    
    Log.debug("%s, retstate = %d" %(cmd, retState))
    if retState == 0: bRet = True
    return bRet


# 管道执行命令， 命令小输出还可以， 如果输出比较大推荐走文件输出流
def exec_cmd(cmd):
    
    Log.debug("cmd: %s" %(cmd))
    content = ""
    try:
        p = Popen(cmd, bufsize = 4096, stdout = PIPE, shell = True)
        
        while True:
            cont = p.stdout.read()
            if cont == "": break
            content += cont
            Log.debug("contLen: %d" %(len(cont)))
            time.sleep(1)
        retState = p.wait()
        
        return retState, content
    except Exception, e:
        Log.err("(%s)" %(traceback.format_exc()))
        return 255, "cmd(%s) err: %s" %(str(cmd), str(e))
    
    
#  进程池   
class YgProcessPool:
    
    def __init__(self, pidNum, fun, args):
        
        self.pool   =   []      # 进程池
        self.size   =   pidNum
        self.fun    =   fun
        self.args   =   args
    
    def start(self, wait = False):
        
        bRet = True
        try:
            for i in range(self.size):
                pid = os.fork()
                if pid == 0:
                    retCode = 0
                    try:
                        bRet = self.fun(i, self.size, self.args)
                        if not bRet: retCode = -1
                    except Exception, e:
                        Log.err("ERR(%s)" %(traceback.format_exc()))
                        retCode = -1
                         
                    os._exit(retCode)
                    #sys.exit(retCode)
                    
                self.pool.append(pid)
            
            if wait:
                bRet = self.wait()
                
        except Exception, e:
            Log.err("ERR(%s)" %(traceback.format_exc()))
            bRet = False
            
        return bRet
    
    def wait(self):
        
        bRet = True
        for i in range(self.size):
            pid, retCode = os.waitpid(self.pool[i], 0)
            if retCode != 0: bRet = False
        return bRet 
    
    
