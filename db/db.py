# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     db
    Description:  初始化db
    Author:       瓦都尅
    Date:         2019/10/31
-----------------------------------
'''
from .redis_client import RedisClient
from conf.setting import *

class Singleton(type):
    """
    Singleton Metaclass http://funhacks.net/2017/01/17/singleton/
    使用元类metaclass实现单例模式singleton，减少资源开销
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args)
        return cls._instances[cls]


class DBclient(object, metaclass=Singleton):

    def __init__(self):
        self.client = RedisClient(name=REDIS_KEY, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def get(self, key, **kwargs):
        return self.client.get(key, **kwargs)

    def put(self, key, **kwargs):
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value, **kwargs)

    def delete(self, key, **kwargs):
        return self.client.delete(key, **kwargs)

    def exists(self, key, **kwargs):
        return self.client.exists(key, **kwargs)

    def getAll(self):
        return self.client.getAll()

    def getCount(self):
        return self.client.getCount()