# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     proxy_manager
    Description:  代理管理
    Author:       瓦都尅
    Date:         2019/10/31
-----------------------------------
'''
import random

from db import db
from util.log_handler import LogHandler
from conf.setting import *
from proxy.get_free_proxyip import GetFreeProxy
from proxy.check_proxy import verifyProxyFormat
from proxy.proxy_info import Proxy


class LazyProperty(object):
    """
    LazyProperty https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p10_using_lazily_computed_properties.html
    使用延迟计算属性来提升性能
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class GetFunctions(object):

    def __init__(self):
        pass

    @LazyProperty
    def proxy_get_functions(self):
        return PROXY_GETTER


class ProxyManager(object):
    def __init__(self):
        self.client = db.DBclient()
        self.log = LogHandler('proxy_manager')

    def fetch(self):
        proxy_set = set()
        self.log.info(u'代理抓取: start')
        get_function = GetFunctions()
        for proxy_get in get_function.proxy_get_functions:
            self.log.info('Get Proxy - {}: start'.format(proxy_get))
            try:
                for proxy in getattr(GetFreeProxy, proxy_get.strip())():
                    proxy = proxy.strip()

                    if not proxy or not verifyProxyFormat(proxy):
                        self.log.error('Get Proxy - {}: {} error'.format(proxy_get,proxy))
                        continue
                    elif proxy in proxy_set:
                        self.log.info('Get Proxy - {}: {} is exist'.format(proxy_get,proxy))
                        continue
                    else:
                        self.log.info('Get Proxy - {}: {} success'.format(proxy_get, proxy))
                        self.client.put(Proxy(proxy, source=proxy_get))
                        proxy_set.add(proxy)

            except Exception as e:
                self.log.error('Get Proxy - {}: error'.format(proxy_get))
                self.log.error(str(e))

    def get(self):
        proxy_list = self.client.getAll()
        if proxy_list:
            proxy = random.choice(proxy_list)
            return Proxy.newProxyFromJson(proxy)
        else:
            return None

    def getAll(self):
        proxy_list = self.client.getAll()
        return [Proxy.newProxyFromJson(_) for _ in proxy_list]

    def getCount(self):
        proxy_counts = self.client.getCount()
        return proxy_counts

    def delete(self, proxy_key):
        self.client.delete(proxy_key)


if __name__ == '__main__':
    pp = ProxyManager()
    proxy = pp.get()
    print(proxy.info_json)