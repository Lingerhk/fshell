# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: MySQL基础操作类封装


import MySQLdb
from fs_log import *

class SqlCmdEnum:
    COMMIT_CMD = 0
    ROLLBACK_CMD = 1
    
class SqlExecEnum:
    QUERY       =   0
    UPDATE      =   1
    INSERT      =   2
    DELETE      =   3
    

def _new_conn(host, port, user, passwd, db, charset):
    try:
        conn = MySQLdb.connect(host = host,
                               port = port,
                               user = user,
                               passwd = passwd,
                               db = db,
                               charset = charset)
        conn.autocommit(True)
        Log.debug("conn(host: %s, port: %d, user: %s, passwd: %s, db: %s)" %(host, port, user, passwd, db))
        return conn
    except Exception, e:
        Log.err("ERR(host: %s, port: %d, user: %s, passwd: %s, db: %s, %s)" %(host, port, user, passwd, db, str(e)))
        return None

class DataBase: 
    
    def __init__(self,               
                 host = BaseConf.SQL_HOST, 
                 port = BaseConf.SQL_PORT,
                 user = BaseConf.SQL_USER,
                 passwd = BaseConf.SQL_PASSWD,
                 db = BaseConf.SQL_DB,
                 charset = None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        
        self.conn = None
        
    def _check(self):
        try:
            self.conn.ping()
        except Exception, e:
            self.conn = _new_conn(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        
    def _get_conn(self):
        if self.conn == None:
            self.conn = _new_conn(self.host, self.port, self.user, self.passwd, self.db, self.charset)
        else: 
            self._check()
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            

    def _get_record_list(self, cursor):
        
        def _get_fieldname_list(cursor):
            fieldList = []
            for info in cursor.description:
                fieldList.append(info[0])
            return fieldList
        
        fieldnameList = _get_fieldname_list(cursor)
        
        retNodeList = []
        recordList = cursor.fetchall()
        for record in recordList:
            node = {}
            for i in range(len(fieldnameList)):
                node[fieldnameList[i]] = record[i]
            retNodeList.append(node)
        
        return retNodeList
            
        
    def _exec_cmdstr(self, cmdstr, param, rollback, execType):
        
        def _encode_param(param):
            dParam = []
            for par in param:
                if type(par) == unicode:
                    par = par.encode('utf-8')
                dParam.append(par)
            return dParam
        
        if param != None:  param = _encode_param(param)
        Log.debug("%s\t%s" %(cmdstr, str(param)))
        
        self._get_conn()
        conn = self.conn
        if conn == None:
            Log.err("mysql not connect!")
            return False, "mysql not connect!"
        
        cursor = conn.cursor()
        try:
            val = cursor.execute(cmdstr, param)
            if execType == SqlExecEnum.QUERY:    val = self._get_record_list(cursor)
            elif execType == SqlExecEnum.INSERT: val = int(conn.insert_id())
            else: pass
        except Exception, e:
            Log.warning("sql: %s,%s ERR(%s)" %(cmdstr, str(param), str(e)))
            if rollback:
                self.cmd_submit(SqlCmdEnum.ROLLBACK_CMD)
            else:
                self._close_conn()        
            return False, "%s:%s %s" %(cmdstr, str(param), str(e))

        if not rollback:
            self._close_conn()
        
        return True, val
    
    def query_data(self, cmdstr, param, rollback = False):
        return self._exec_cmdstr(cmdstr, param, rollback, SqlExecEnum.QUERY)
    
    def update_data(self, cmdstr, param, rollback = False):
        return self._exec_cmdstr(cmdstr, param, rollback, SqlExecEnum.UPDATE)
        
    def insert_data(self, cmdstr, param, rollback = False):
        return self._exec_cmdstr(cmdstr, param, rollback, SqlExecEnum.INSERT)
    
    def delete_data(self, cmdstr, param, rollback = False):
        return self._exec_cmdstr(cmdstr, param, rollback, SqlExecEnum.DELETE)
    
    def cmd_submit(self, flag):
        conn = self.conn
        if not conn: self._close_conn(); return
        
        try:
            if flag == SqlCmdEnum.COMMIT_CMD:
                conn.commit()
            elif flag == SqlCmdEnum.ROLLBACK_CMD:
                conn.rollback()
        finally:
            self._close_conn()
            

if __name__ == "__main__":
    
    dataBase = DataBase()
    
    cmdstr = "select * from tb_user limit 10"
    print dataBase.query_data(cmdstr, None)
