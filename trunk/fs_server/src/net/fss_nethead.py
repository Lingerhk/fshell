# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-09
# desc: 完成数据包编/解码


import socket
import sys
import os
import time

from fs_log import *


class NetHead:
    
    START_CODE = 0x11111111
    
    def __init__(self):
        self.start = 0
        self.type = 0
        self.pkgLen = 0

    @staticmethod
    def size():
        return 9
    
    @staticmethod
    def str2int(s):
        if len(s) < 4: return None
        
        a = s[0 : 1]
        b = s[1 : 2]
        c = s[2 : 3]
        d = s[3 : 4]
        
        ts = (ord(a) << 24) + (ord(b) << 16) + (ord(c) << 8) + ord(d)
        return ts
    
    @staticmethod
    def int2str(n):
        
        d = n & 0xff; n = n >> 8;
        c = n & 0xff; n = n >> 8;
        b = n & 0xff; n = n >> 8;
        a = n & 0xff; n = n >> 8;
        
        ts = chr(a) + chr(b) + chr(c) + chr(d)
        return ts 
    
     
    @staticmethod
    def decode(data):
        
        if data == None or len(data) < 9:
            Log.err("data: %s is not valid!" %(str(data)))
            return None
        
        netHead = NetHead()
        netHead.start = NetHead.str2int(data[0 : 4])
        netHead.type = ord(data[4 : 5])
        netHead.pkgLen = NetHead.str2int(data[5 : 9])
        
        if netHead.start != NetHead.START_CODE: 
            Log.err("netHead not valid(%d, %d, %d)" %(netHead.start, netHead.type, netHead.pkgLen));
            return None
        
        Log.debug("netHead(start=%d, type=%d, pkgLen=%d)" %(netHead.start, netHead.type, netHead.pkgLen));
        return netHead
    
    
    @staticmethod
    def encode(netHead):
        start = NetHead.int2str(netHead.start)
        type = chr(netHead.type)
        pkgLen = NetHead.int2str(netHead.pkgLen)
        cnt = start + type + pkgLen
        
        Log.debug("netHead_encode: cnt_len: %d" %(len(cnt)))
        return cnt
