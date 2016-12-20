# -*- coding: UTF-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: 基础常规方法封装


from fs_log import *
from fs_time import *

import hashlib
import zipfile
import csv
import cStringIO
import urllib

def get_guid():
    guid = str(uuid.uuid1())
    return guid


#  递归的获取path下面的所有文件全名（不包括目录）
def get_file(path):
    retList = []
    if os.path.exists(path) and os.path.isdir(path):
        childList = os.listdir(path)
        for childName in childList:
            childFullName = "%s/%s" % (path, childName)
            if os.path.isfile(childFullName):
                retList.append(childFullName)
            elif os.path.isdir(childFullName):
                retChildList = get_file(childFullName)
                for retChildPath in retChildList:
                    retList.append(retChildPath)
    else:
        Log.err("please check dir(%s) path")

    return retList


def rm_file(path, delflag=False):
    if not path: return
    if not os.path.exists(path): return

    if os.path.isfile(path):
        os.unlink(path)
        return

    fileList = os.listdir(path)
    if len(fileList) != 0:
        for fname in fileList:
            filePath = "%s/%s" % (path, fname)
            rm_file(filePath, True)

    if delflag:
        os.rmdir(path)


def cp_file(sfile, dfile):
    bRet = True
    rfp = None;
    wfp = None
    try:
        rfp = open(sfile, "rb")
        wfp = open(dfile, "wb")
        wfp.write(rfp.read())
    except Exception, e:
        Log.err("_cpfile(%s, %s) ERR(%s)" % (sfile, dfile, str(e)))
        bRet = False
    finally:
        if rfp != None: rfp.close()
        if wfp != None: wfp.close()
    return bRet


def get_file_line(fPath):
    cmd = "cat %s | wc -l" % (fPath)
    iRet, sRet = exec_cmd(cmd)
    if iRet != 0:  return -1
    try:
        return int(sRet)
    except Exception, e:
        Log.err("%s is not valid" % (sRet))
        return -1


def cp_dir(fromDir, toDir):
    if not os.path.exists(toDir):  os.makedirs(toDir)

    fnameList = os.listdir(fromDir)
    for fname in fnameList:
        fromFile = "%s/%s" % (fromDir, fname)
        toFile = "%s/%s" % (toDir, fname)
        if os.path.isfile(fromFile):
            bRet = cp_file(fromFile, toFile)
            if not bRet:  return False
        if os.path.isdir(fromFile):
            bRet = cp_dir(fromFile, toFile)
            if not bRet:  return False
    return True


def get_dict(dictObj, key, default=None):
    if not isinstance(dictObj, dict):
        return None
    if not dictObj.has_key(key):
        return default
    return dictObj[key]


def compute_md5_file(fileName):
    try:
        md5 = hashlib.md5()
        fp = open(fileName, "rb")

        while True:
            data = fp.read(8192)
            if not data: break
            md5.update(data)

        fp.close()
        sret = md5.hexdigest().upper()
        return sret

    except Exception, e:
        Log.err("fileName(%s) ERR(%s)" % (fileName, str(e)))
        return None


def comput_md5_text(text):
    try:
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest().upper()
    except Exception, e:
        Log.err("md5(%s) ERR(%s)" % (text, str(e)))
        return None


# json load, 结果为UTF-8
def json_loads_utf8(cont):
    def decode(jsonCont):

        if type(jsonCont) == unicode:
            return jsonCont.encode("utf-8")

        if type(jsonCont) == tuple or type(jsonCont) == list:
            for i in range(len(jsonCont)):
                jsonCont[i] = decode(jsonCont[i])
            return jsonCont

        if type(jsonCont) == dict:
            retJsonCont = {}
            for key in jsonCont:
                retJsonCont[decode(key)] = decode(jsonCont[key])
            return retJsonCont

        return jsonCont

    if cont == None or cont == "":
        return None

    jsonCont = json.loads(cont)
    return decode(jsonCont)


# xml => json
class XmlToJson:
    def __init__(self):
        self.jRootNode = {}

    @staticmethod
    def _decode(value):
        if type(value) == unicode:
            return value.encode("utf-8")
        return str(value)

    def _change(self, node):

        if node == None or node.tag == None:  return None

        retJson = {
            "tag": re.sub("\t", " ", XmlToJson._decode(node.tag)),
            "text": re.sub("\t", " ", XmlToJson._decode(node.text)),
            "attrib": {},
            "_children": [],
        }

        for childNode in node._children:
            childNode = self._change(childNode)
            retJson["_children"].append(childNode)

        for attrName in node.attrib:
            retJson["attrib"][attrName] = re.sub("\t", " ", XmlToJson._decode(node.attrib[attrName]))

        return retJson

    def change_text(self, textCnt):

        try:
            from xml.etree import ElementTree as ET
            rootNode = ET.fromstring(textCnt)
            self.jRootNode = self._change(rootNode)
        except Exception, e:
            Log.err("TEXT(%s) ERR(%s)" % (textCnt, str(e)))
            return False

        return True

    def get_jsontext(self):
        return json.dumps(self.jRootNode)

    def get_attr(self, jnode, key):

        if jnode == None: return None
        if type(jnode) != dict: return None
        if type(jnode["attrib"]) != dict: return None
        if key == None:  return None
        if jnode["attrib"].has_key(key) == False: return None

        return jnode["attrib"][key]

    def get_value(self, jnode, key):

        if jnode == None: return None
        if type(jnode) != dict: return None
        if type(jnode["_children"]) != list: return None
        if key == None:  return None

        for jchildNode in jnode["_children"]:
            if jchildNode["tag"] == key:
                return jchildNode["text"]

        return None


# xml => json
# 用于xml没有attr的特殊场景, 为了简化调用者
# 为了方便，丧失顶层TAG的保存
class XmlToJson2:
    def __init__(self):
        self.jRootNode = {}

    def _change(self, node):

        # 去除\t, \n, 首尾空白字符。如果不为空则用utf-8.encode. 否则返回None
        def _encode_cnt(value):
            if value == None or value == "": return None

            value = re.sub("\t|\n", " ", value)

            if type(value) == unicode:
                value = value.encode("utf-8")

            value = value.strip()
            if value == "": return None
            return value

        if node == None or node.tag == None:  return None
        text = _encode_cnt(node.text)
        if text != None:    return text

        retJson = {}
        for childNode in node._children:
            childTag = _encode_cnt(childNode.tag)
            if childTag == None: continue
            childVal = self._change(childNode)
            # if childVal == None: continue
            retJson[childTag] = childVal
        return retJson

    def change_text(self, textCnt):

        try:
            from xml.etree import ElementTree as ET
            rootNode = ET.fromstring(textCnt)
            self.jRootNode = self._change(rootNode)
        except Exception, e:
            Log.err("TEXT(%s) ERR(%s)" % (textCnt, str(e)))
            return False

        return True

    def get_jsontext(self):
        return json.dumps(self.jRootNode)

    def get_value(self, jnode, key):

        if not jnode.has_key(key):  return None
        return jnode[key]


def yg_zipfile_1(fPath, storePath, password=None):
    if not os.path.exists(fPath):
        Log.err("filePath = %s is not exist" % (fPath))
        return False
    if not os.path.exists(storePath):
        try:
            os.makedirs(storePath)
        except Exception, e:
            Log.err("os.makedirs(%s) ERR(%s)" % (storePath, str(e)))
    else:
        rm_file(storePath)

    bRet = True
    f = None
    try:
        f = zipfile.ZipFile(fPath)
        if password != None:
            f.setpassword(password)
        f.extractall(storePath)
    except Exception, e:
        Log.err("zipfile(%s, %s) ERR(%s)" % (fPath, storePath, str(e)))
        bRet = False
    finally:
        if f != None: f.close()
    return bRet


def yg_zipfile(fPath, storePath, password=None):
    if not os.path.exists(fPath):
        Log.err("filePath = %s is not exist" % (fPath))
        return False
    if not os.path.exists(storePath):
        try:
            os.makedirs(storePath)
        except Exception, e:
            Log.err("os.makedirs(%s) ERR(%s)" % (storePath, str(e)))
    else:
        rm_file(storePath)

    if password != None:
        zipCmd = "unzip -P %s %s -d %s" % (password, fPath, storePath)
    else:
        zipCmd = "unzip %s -d %s" % (fPath, storePath)

    return bs_system(zipCmd)


def yg_untar(fPath, storePath):
    if not os.path.exists(fPath):
        Log.err("filePath = %s is not exist" % (fPath))
        return False
    if not os.path.exists(storePath):
        try:
            os.makedirs(storePath)
        except Exception, e:
            Log.err("os.makedirs(%s) ERR(%s)" % (storePath, str(e)))

    unTarCmd = "tar -zxvf %s -C %s" % (fPath, storePath)

    return bs_system(unTarCmd)


def yg_encode_check(cnt):
    import chardet
    enc = chardet.detect(cnt)
    return enc['confidence'], enc['encoding']


def try_decode(cnt):
    def decode(cnt, coding):
        try:
            return cnt.decode(coding)
        except:
            return None

    dcnt = decode(cnt, "utf-8")
    if dcnt != None: return dcnt

    dcnt = decode(cnt, "gbk")
    if dcnt != None: return dcnt

    return None


def try_change(cnt, coding="utf-8"):
    dcnt = try_decode(cnt)
    if dcnt == None: return None

    return dcnt.encode(coding)


def regexp_extract(source, matchStr, num):
    try:
        matchObj = re.search(matchStr, source)
        if not matchObj: return None
        return matchObj.group(num)

    except Exception, e:
        Log.err("source(%s), matchStr(%s),num(%d) Err(%s)" % (source, matchStr, num, str(e)))
        return None


class Page(object):
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index < 1) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (
            self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)


def safe_json_loads(jsonData):
    try:
        return json.loads(jsonData)
    except Exception, e:
        Log.err(traceback.format_exc())
        return None


def safe_datetime_to_str(tm):
    if type(tm) == datetime.datetime:
        return tm.strftime("%Y-%m-%d %H:%M:%S")
    return ''


def safe_str_split(string, sep):
    try:
        return string.split(sep)
    except Exception, e:
        return []

def html_decode(string):
    return urllib.unquote(string)


def check_ip_format(ip_data, format):
    """
    check ip format: ip(10.0.0.1), (mask)10.0.0.1/24, (segment)10.0.0.1-10.0.0.54
    """
    if format == 'ip':
        pic = ip_data.split('.')
        if len(pic) != 4: return False
        try:
            return all(0 <= int(p) < 256 for p in pic)
        except ValueError:
            return False

    elif format == 'mask':
        
        ips = ip_data.split('/')
        if len(ips) != 2: return False
        if (int(ips[1]) < 0) or (int(ips[1]) > 32): return False

        pic = ips[0].split('.')
        if len(pic) != 4: return False
        try:
            return  all(0 <= int(p) < 256 for p in pic)
        except ValueError:
            return False

    elif format == 'segment':
        ips = ip_data.split('-')
        if len(ips) != 2: return False

        pic = ips[0].split('.')
        pic.extend(ips[1].split('.'))

        if len(pic) != 8: return False
        try:
            return all(0 <= int(p) < 256 for p in pic)
        except ValueError:
            return False

    else:
        return False

class GetIpSegment(object):
    """
    format ip/mask to an ip segment.
    eg: '192.168.1.5/26' to '192.168.1.0-192.168.1.63'
    """

    def __init__(self, ip_mask):
        self.ip_mask = ip_mask

    def dec2bin(self, n):
        bin_str = bin(n).replace("0b", "")
        z_str = ''.join([str('0') for x in range(8-len(bin_str))])
        return z_str + bin_str

    def bin2ip_str(self, bin_str):
        ip = []
        for i in range(0, len(bin_str), 8):
            dec_str = str(int(bin_str[i:i+8], 2)) # bin2dec
            ip.append(dec_str)
        return ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3]

    def ip_str(self):

        ip = self.ip_mask.split("/")[0]
        mask = int(self.ip_mask.split("/")[1])
        ip_lt = ip.split(".")
        ip_bin = ''.join([self.dec2bin(int(x)) for x in ip_lt])
        ip_bin_p = ip_bin[0:mask]

        ip_min = ip_bin_p + ''.join([str('0') for i in range(32-mask)])
        ip_max = ip_bin_p + ''.join([str('1') for i in range(32-mask)])
                                    
        return (self.bin2ip_str(ip_min), self.bin2ip_str(ip_max))


class Echo(object):
    def write(self, value):
        return value


class CSVWriter:
    """
    A CSV writer which will write rows to CSV file "f"
    """

    def __init__(self, f=None, dialect=csv.excel, **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f if f else Echo()

    def writerow(self, row):
        self.writer.writerow(row)
        data = self.queue.getvalue()
        value = self.stream.write(data)
        self.queue.truncate(0)
        return value

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    def test1():
        print yg_encode_check(u'我们都有一个家'.encode('gbk'))
        print yg_encode_check(u'我们都有一个家'.encode('utf-8'))
        print yg_encode_check("zxy")


    def test2():
        print try_change(u'我们都有一个家'.encode('gbk'))


    def test3():
        print get_file_line(os.path.abspath("../../data/ftp_root/test1"))


    # test2()
    # test3()
    #print GetIpSegment('192.168.1.1/0').ip_str()
