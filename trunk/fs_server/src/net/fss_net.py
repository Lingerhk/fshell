# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-09
# desc: 完成网络接收，并存入mysql


import select
from fss_cfg import *
from fss_nethead import *


''' 
    目的：监听端口，完成解码进行回调
    server, 提供事件驱动，但采用阻塞模式
'''

class FsNetMode:
    T_SYN_MODE      =   0       # 请求应答模式
    T_ASY_MODE      =   1       # 异步模式
    

class FsNetConf:
    
    def __init__(self):
        self.ip = None
        self.port = None
        self.mode = None
        self.acceptFun = None
        self.pkgFun = None
        self.closeFun = None
        
class FsSession:
    
    class Status:
        T_ACCEPT            =   0
        T_CONNECTING        =   1
    
    def __init__(self):
        self.ip = None
        self.port = None
        self.sock = -1
        self.conf =None
        self.status = None
        self.extra = None
    
    @staticmethod
    def new_session(sock, ip, port, status, conf):
        session = FsSession()
        session.ip = ip
        session.port = port
        session.sock = sock
        session.status = status
        session.conf = conf
        session.buf = ""
        
        return session
    

class FsNet:
    
    READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
    
    def __init__(self):
        self.confList  = []
        self.sessionMap = {}
        self.poller = select.poll()
        
    
    def append(self, ip, port, mode, acceptFun, pkgFun, closeFun):
        node = FsNetConf()
        node.ip = ip
        node.port = port
        node.mode = mode
        node.acceptFun = acceptFun
        node.pkgFun = pkgFun
        node.closeFun = closeFun
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.listen(1024)
        session = FsSession.new_session(sock, ip, port, FsSession.Status.T_ACCEPT, node)
        self.sessionMap[session.sock.fileno()] = session
        
        self.poller.register(session.sock, FsNet.READ_ONLY)
        self.confList.append(node)
        
        return True, ""
    
    
    def _accept_conn(self, session, conf):
        conn, clientAddr = session.sock.accept()
        ip, port = clientAddr
        
        cliSession = FsSession.new_session(conn, ip, port, FsSession.Status.T_CONNECTING, conf)
        
        if conf.acceptFun != None:
            bAccept = conf.acceptFun(session, cliSession)
            if not bAccept:
                conn.close()
                Log.info("srv(%s, %d) not accept(%s, %d)" %(session.ip, session.port, ip, port))
                return True, ""
        
        self.sessionMap[conn.fileno()] = cliSession
        self.poller.register(cliSession.sock, FsNet.READ_ONLY)
        
        return True, ""
    
    
    def _close_session(self, session, conf):
        if session.status == FsSession.Status.T_ACCEPT:
            Log.err("server sock(%s, %d) ERR!...." %(session.ip, session.fd))
            return 
        
        if conf.closeFun != None:
            conf.closeFun(session)
        
        if session.sock != None:
            self.poller.unregister(session.sock)
            del self.sessionMap[session.sock.fileno()]
            session.sock.close() 
            session.sock = None
     
     
    def _deal_pkg(self, session, conf, packet, bodyType):
        try:
            #Log.debug("deal_pkg: %s" %(packet))
            packet = unicode(packet, errors='ignore')
            reqJson = json.loads(packet)
            if conf.pkgFun != None:
                return conf.pkgFun(session, reqJson)
            
        except Exception, e:
            Log.err(traceback.format_exc())
            return False, str(e)
        
        return True, "" 
    
    # 接收一个完整的数据包， 如果包不合法直接短链接        
    def _read_pkg(self, session, conf):
        
        sock = session.sock
        buf = sock.recv(16 * 1024)
        if buf == None or len(buf) == 0:
            self._close_session(session, conf)
            return False, "client close connection"

        buf = session.buf + buf
        session.buf = ""

        while True:
            if len(buf) < NetHead.size():
                session.buf = buf
                #self._close_session(session, conf)
                return True, ""
                #return False, "buf_len: %d < len(NetHead)" %(len(buf))
            
            netHead = NetHead.decode(buf)
            if netHead == None:
                self._close_session(session, conf)
                return False, "NetHead.decode ERR"
                
            pkgLen = netHead.pkgLen
            while len(buf) < pkgLen:
                sock.settimeout(3)
                val = sock.recv(16 * 1024)
                sock.settimeout(None)
                if val == None or len(val) == 0:
                    self._close_session(session, conf)
                    return False, "client close connection"
                
                buf = buf + val
            
            packet = buf[NetHead.size() : pkgLen]
            bRet, sRet = self._deal_pkg(session, conf, packet, netHead.type)
            if not bRet:
                Log.err("_deal_pkg ERR(%s)!" %(str(sRet)))
                self._close_session(session, conf) 
                return False, "_deal_pkg ERR(%s)!" %(str(sRet))
            
            if len(buf) > pkgLen:
                buf = buf[pkgLen : len(buf)]
                continue
            
            return True, ""
            
    def send_req(self, session, cmdInfo):
        
        netHead = NetHead()
        netHead.start = NetHead.START_CODE
        netHead.type = 0
        netHead.pkgLen = len(cmdInfo) + NetHead.size()
        headStr = NetHead.encode(netHead) 
        rspStr = headStr + cmdInfo
        
        sendlen = session.sock.send(rspStr)    
        Log.debug("sendLen: %d" %(sendlen))
        
        return True, ""
    
    
    def run(self):
        
        while True:
            events = self.poller.poll(1000)
            for fd, flag in events:
                try:
                    print fd, flag
                    if not self.sessionMap.has_key(fd):
                        continue

                    session = self.sessionMap[fd]
                    conf = session.conf

                    if flag & select.POLLIN or flag & flag & select.POLLPRI:
                        if session.status == FsSession.Status.T_ACCEPT:

                            bRet, sRet = self._accept_conn(session, conf)
                            if not bRet: 
                                Log.err("accept_conn ERR: %s" %(sRet))
                        else:
                            bRet, sRet = self._read_pkg(session, conf)
                            if not bRet:
                                Log.err("_read_req(%s, %d) conf:(%s, %d) ERR: %s" %(session.ip, session.port, conf.ip, conf.port, sRet))

                            if conf.mode == FsNetMode.T_SYN_MODE:
                                self._close_session(session, conf)


                    elif flag & select.POLLHUP or flag & select.POLLERR:
                        self._close_session(session, conf)

                except Exception, e:
                    Log.err("%s, %s" %(traceback.format_exc(), str(e)))
                    
                    
    def close_session(self, session):
        conf = session.conf
        self._close_session(session, conf)

                    
                    
g_fsNet = FsNet()
