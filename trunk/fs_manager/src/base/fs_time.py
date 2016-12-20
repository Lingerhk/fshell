# -*- coding: UTF-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-08
# desc: 时间处理类封装


from fs_log import *
import datetime
import time


def get_cur_dtime():
    return int(time.time())


def get_cur_time(tmFormat=None):
    if tmFormat == None: tmFormat = "%Y-%m-%d %H:%M:%S"
    return (datetime.datetime.now()).strftime(tmFormat)


def yg_tm_str_int(strTm, format="%Y-%m-%d %H:%M:%S"):
    if type(strTm) == datetime.datetime:
        strTm = strTm.strftime(format)
    tmTuple = time.strptime(strTm, format)
    return time.mktime(tmTuple)


def yg_tm_int_str(tm, format="%Y-%m-%d %H:%M:%S"):
    # tmObj = time.localtime(tm)
    tmObj = time.localtime(tm)
    return time.strftime(format, tmObj)


def get_cur_day(days=0, format="%Y%m%d"):
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime(format)


def get_cur_time_2(days=0, format="%Y-%m-%d %H:%M:%S"):
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime(format)


def get_latest_months():
    latest_months = []
    now = datetime.datetime.now()
    for i in range(9):
        latest_months.append((now.year, now.month))
        now = now - datetime.timedelta(days=now.day)
    return latest_months


def format_time_string(timestamp, now=None):
    if now is None:
        now = datetime.datetime.now().strftime("%s")
    ts_delta = int(now) - int(timestamp)
    if ts_delta < 60:
        return u"%d秒" % int(ts_delta)
    elif 60 <= ts_delta < 3600:
        return u"%d分%d秒" % (int(ts_delta // 60), int(ts_delta % 60))
    elif 3600 <= ts_delta < 86400:
        return u"%d小时%d分" % (int(ts_delta // 3600), int((ts_delta % 3600) / 60))
    elif 86400 <= ts_delta < 2678400:
        return u"%d天%d小时" % (int(ts_delta // 86400), int((ts_delta % 86400) / 3600))
    elif 2678400 <= ts_delta < 8035200:
        return u"%d月%d天" % (int(ts_delta // 2678400), int((ts_delta % 2678400) / 86400))
    else:
        return u"%d年%d月" % (int(ts_delta // 8035200), int((ts_delta % 8035200) / 2678400))


def format_time_string_v2(timestamp):
    now = datetime.datetime.now().strftime("%s")
    ts_delta = int(now) - int(timestamp)
    if ts_delta < 60:
        return u"刚刚"
    elif 60 <= ts_delta < 3600:
        return u"%d分钟前" % int(ts_delta / 60)
    elif 3600 <= ts_delta < 86400:
        return u"%d小时前" % int(ts_delta / 3600)
    elif 86400 <= ts_delta < 2678400:
        return u"%d天前" % int(ts_delta / 86400)
    elif 2678400 <= ts_delta < 8035200:
        return u"%d月前" % int(ts_delta / 2678400)
    else:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


if __name__ == "__main__":
    def test1():
        print get_cur_time_2(1, "%Y-%m-%d 00:00:00")


    def test2():
        print datetime.datetime.now() - datetime.timedelta(0)


    def test3():
        tm = time.time()
        tm = int(tm / (24 * 3600)) * (24 * 3600)

        print yg_tm_int_str(tm)


    def test4():
        print time.localtime(time.time()).tm_hour
        print time.gmtime(time.time() + 8 * 3600)


    def test5():
        curTm = get_cur_dtime()
        print curTm
        print yg_tm_str_int(get_cur_time())
        print get_cur_time()
        print yg_tm_int_str(curTm)


    def test6():
        print yg_tm_int_str(1406131980)


    def test7():
        print get_latest_months()

    def test8():
        print get_cur_day(7, "%Y-%m-%d %H:%M:%S")
    # test7()
    #test8()

    print get_cur_day(-2,format="%Y-%m-%d")
