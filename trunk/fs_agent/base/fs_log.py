# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-11
# desc: 标准log模块


from fs_syshead import *

class LogLevel:
    DEBUG   =   1
    INFO    =   2
    WARNING =   3
    ERR     =   4
    ALERT   =   5
    CLOSE   =   10
    
def _get_log_level(logLevel):
    if logLevel == LogLevel.DEBUG:      return "DEBUG"
    if logLevel == LogLevel.INFO:       return "INFO"
    if logLevel == LogLevel.WARNING:    return "WARNING"
    if logLevel == LogLevel.ERR:        return "ERROR"
    if logLevel == LogLevel.ALERT:      return "ALERT"
    return "CLOSE"

def _get_log_tm():
    "[01/Jan/2013 04:51:46]"
    return (datetime.datetime.now()).strftime("[%d/%m/%Y %H:%M:%S]")


def _get_file(f):       return f[1]
def _get_function(f):   return f[3]
def _get_line(f):       return f[2]
def _get_location(stackIdx):
    f = inspect.stack()[stackIdx]
    return "%s::%s(%d)" %(_get_file(f), _get_function(f), _get_line(f))
   
   
class LogFile:
    
    @staticmethod
    def rm_file(path, delflag = False):
        
        if not path: return
        if not os.path.exists(path): return
        
        if os.path.isfile(path):
            os.unlink(path)
            return
        
        fileList = os.listdir(path)
        if len(fileList) != 0:
            for fname in fileList:
                filePath = "%s/%s" %(path, fname)
                LogFile.rm_file(filePath, True)
        
        if delflag:            
            os.rmdir(path)
    
    def __init__(self):
        #LogFile.rm_file(BaseConf.LOG_DIR)
        
        self.fp = None;
        #self.maxLine = 1024
        #self.fIdx = 0
        self.maxSzie    =   1024 * 1024
        self.fName = -1
        
    def _open_logfile(self):
        self.fName += 1
        if not os.path.exists(BaseConf.LOG_DIR):
            os.makedirs(BaseConf.LOG_DIR)
        
        curTm = (datetime.datetime.now()).strftime("%Y_%m_%d_%H_%M_%S")
        preFix = BaseConf.LOG_PREFIX + "_%s" %(curTm)
        #tmpName = "%s/%d.txt" %(BaseConf.LOG_DIR, self.fName)
        tmpName = "%s/%s.txt" %(BaseConf.LOG_DIR, preFix)
        
        try:
            if self.fp:  self.fp.close()
            self.fp = open(tmpName, "a")
            #self.fIdx = 0
            
            os.dup2(self.fp.fileno(), sys.stdout.fileno())
            os.dup2(self.fp.fileno(), sys.stderr.fileno())
        except Exception, e:
            sys.stderr.write("%s: %s\n" %(_get_location(1), str(e)))
                
    def _print_log(self, buf):
        try:
            #if self.fp == None or self.fIdx >= self.maxLine:
            if self.fp == None or self.fp.tell() >= self.maxSzie:
                self._open_logfile()
            
            self.fp.write(buf)
            self.fp.flush()
            #self.fIdx += 1
                 
        except Exception, e:
            sys.stderr.write("%s: %s" %(_get_location(1), str(e)))
            sys.stderr.flush()   

logFile = LogFile()

   
class Log:
    
    @staticmethod
    def _loglog(buf, stackIdx, logLevel):
        if logLevel >= BaseConf.LOG_LEVEL:
            msg = "%s[%s]%s: %s\n"  %(_get_log_tm(), _get_log_level(logLevel), _get_location(stackIdx + 1), buf)
            if BaseConf.IS_CTR_LOG:   sys.stderr.write(msg); sys.stderr.flush() 
            else:   logFile._print_log(msg)
            
            
    @staticmethod
    def debug(buf, stackIdx = 1):
        Log._loglog(buf, stackIdx + 1, LogLevel.DEBUG)
        
    @staticmethod
    def info(buf, stackIdx = 1):
        Log._loglog(buf, stackIdx + 1, LogLevel.INFO)    
        
    @staticmethod
    def warning(buf, stackIdx = 1):
        Log._loglog(buf, stackIdx + 1, LogLevel.WARNING) 
        
    @staticmethod
    def err(buf, stackIdx = 1):
        Log._loglog(buf, stackIdx + 1, LogLevel.ERR) 
        
    @staticmethod
    def alert(buf, stackIdx = 1):
        Log._loglog(buf, stackIdx + 1, LogLevel.ALERT) 
        
        
if __name__ == "__main__":
    Log.debug("Test......")
    Log.info("Test.......")
    Log.err("Test.......") 
    
    
