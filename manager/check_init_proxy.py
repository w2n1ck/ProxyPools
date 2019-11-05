# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     check_init_proxy
    Description:  初始化代理
    Author:       瓦都尅
    Date:         2019/11/1
-----------------------------------
'''
from socket import socket, AF_INET, SOCK_STREAM
import requests
from threading import Thread
from queue import Queue, Empty
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from util.log_handler import LogHandler
from manager.proxy_manager import ProxyManager
from proxy.proxy_info import Proxy


def tcp_connect(proxy):
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


def valid_request(proxy):
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf-8')
    proxies = {
        "http": "http://{}".format(proxy)
    }
    try:
        r = requests.get('http://icanhazip.com/', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200:
            return True
    except Exception as e:
        pass
    return False


FAIL_COUNT = 0


def check_proxy_useful(proxy_obj):
    if valid_request(proxy_obj.proxy):
        proxy_obj.check_count += 1
        proxy_obj.last_status = 1
        proxy_obj.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if proxy_obj.fail_count > 0:
            proxy_obj.fail_count -= 1
        return proxy_obj, True
    else:
        proxy_obj.check_count += 1
        proxy_obj.last_status = 0
        proxy_obj.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proxy_obj.fail_count += 1
        return proxy_obj, False


class Check(ProxyManager, Thread):

    def __init__(self, queue, thread_name):
        ProxyManager.__init__(self)
        Thread.__init__(self, name=thread_name)
        self.queue = queue
        self.log = LogHandler('init_proxy_check')

    def run(self):
        self.log.info('Init Proxy Check - {} : start'.format(self.name))
        while True:
            try:
                proxy_key = self.queue.get(block=False)
            except Empty:
                self.log.info('Init Proxy Check - {} : end'.format(self.name))
                break

            proxy_obj = Proxy.newProxyFromJson(proxy_key)
            proxy_obj, status = check_proxy_useful(proxy_obj)

            if status:
                self.log.info('Init Proxy Check - {}: {} validation pass'.format(self.name, proxy_obj.proxy))
                self.client.put(proxy_obj)
            else:
                self.log.info('Init Proxy Check - {}: {} validation fail'.format(self.name, proxy_obj.proxy))
                self.client.delete(proxy_obj.proxy)
            self.queue.task_done()


def init_queue_check():
    proxy_queue = Queue()
    pm = ProxyManager()

    for proxy in pm.client.getAll():
        proxy_queue.put(proxy)

    thread_list = list()

    for i in range(10):
        thread_list.append(Check(proxy_queue, "thread_{}".format(i)))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    queue_check()