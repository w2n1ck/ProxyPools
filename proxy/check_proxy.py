# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     check_proxy
    Description:  验证代理格式
    Author:       瓦都尅
    Date:         2019/10/30
-----------------------------------
'''
import re

from proxy.get_free_proxyip import GetFreeProxy
from util.log_handler import LogHandler

log = LogHandler('check_proxy', file=False)


def verifyProxyFormat(proxy):
    """
    检查代理格式
    """
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


class CheckProxy(object):
    @staticmethod
    def checkAllGetProxyFunc():
        """
        检查get_free_proxyip所有代理获取函数运行情况
        """
        import inspect
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_count_dict = dict()
        for func_name, func in member_list:
            log.info(u"开始运行代理抓取函数: {}".format(func_name))
            try:
                proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                log.info(u"获取代理抓取函数: {} 运行出错!".format(func_name))
                log.error(str(e))
        log.info("***" * 5 + u"所有代理抓取函数运行完毕 " + "***" * 5)
        for func_name, func in member_list:
            log.info(u"函数: {n}获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))
