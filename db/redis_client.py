# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     dbclient
    Description:  redis操作
    Author:       瓦都尅
    Date:         2019/10/31
-----------------------------------
'''
from redis.connection import BlockingConnectionPool
from redis import Redis


class RedisClient(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.conn = Redis(connection_pool=BlockingConnectionPool(**kwargs))

    def get(self, proxy_key):
        data = self.conn.hget(name=self.name, key=proxy_key)
        if data:
            return data.decode('utf-8')
        else:
            return None

    def put(self, proxy_obj):
        data = self.conn.hset(self.name, proxy_obj.proxy, proxy_obj.info_json)
        return data

    def update(self, proxy_obj):
        self.conn.hset(self.name, proxy_obj.proxy, proxy_obj.info_json)

    def delete(self, proxy_key):
        self.conn.hdel(self.name, proxy_key)

    def getAll(self):
        item_dict = self.conn.hgetall(self.name)
        try:
            return [value.decode('utf-8') for key,value in item_dict.items()]
        except:
            return item_dict.values()

    def getCount(self):
        return self.conn.hlen(self.name)

    def exists(self, proxy_key):
        return self.conn.hexists(self.name, proxy_key)