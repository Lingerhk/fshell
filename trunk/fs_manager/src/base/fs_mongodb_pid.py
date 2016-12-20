# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: mongodb连接类底层封装

import pymongo
from fs_base_cfg import *


def _now_conn(host, port, user, passwd, db):
    conn = None
    server = "mongodb://%s:%s@%s:%s/%s" % (user, passwd, host, port, db)
    conn = pymongo.MongoClient(server)
    try:
        #Log.debug("...")
        return conn[db]
    except Exception, e:
        #Log.err("...")
        return None


class DataBase:
    def __init__(self,
                host = BaseConf.MG_HOST,
                port = BaseConf.MGPORT,
                user = BaseConf.MG_USER,
                passwd = BaseConf.MG_PASSWD,
                db = BaseConf.MG_DB):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        
        self.conn = None

    def _get_conn(self):
            return _now_conn(self.host, self.port, self.user, self.passwd, self.db)
        
        return self.conn


    def _close_conn(self):
        if self != None:
            self.conn.disconnect()
            self.conn = None


    def insert_data(self, coll, datas):
        conn = self._get_conn()
        coll = conn[coll]
        return coll.insert(datas)

    def update_data(self, col, datas):
        col = self.conn["%s"] % (col)
        return col.update({'name':'steven1'},{'$set':{'realname':'测试1修改'}}, False,False)


    def delete_data(self, coll, datas):
        coll = self.conn["%s"] % (coll)
        return coll.remove({'name':'steven1'})

    def query_data(self, col, datas):
        pass





if __name__ == '__main__':
    db = DataBase()
    datas = [{"username":"s0nnet", "pswd": "qwe@123"}, {"username":"admin", "pswd":"qwe@1234"}]
    print db.insert_data('user', datas)

