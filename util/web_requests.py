# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     web_requests
    Description:  网页请求
    Author:       瓦都尅
    Date:         2019/10/30
-----------------------------------
'''
from requests.models import Response
import requests
import random
import time
from requests.exceptions import ConnectionError
from conf.setting import ua_list, TIMEOUT, RETRY_TIME, RETRY_INTERVAL


class webRequest(object):
    def __init__(self, *args, **kwargs):
        pass

    @property
    def user_agent(self):
        return random.choice(ua_list)

    @property
    def header(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def get(self, url, header=None, retry_flag=list(), *args, **kwargs):

        headers = self.header
        retry_time = RETRY_TIME
        timeout = TIMEOUT
        retry_interval = RETRY_INTERVAL
        if header and isinstance(header, dict):
            headers.update(header)

        while True:
            try:
                html = requests.get(url, headers=headers, timeout=timeout, **kwargs)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html
            except Exception as e:
                print(e)
                retry_time -= 1
                if retry_time <= 0:
                    resp = Response()
                    resp.status_code = 200
                    return resp
                time.sleep(retry_interval)
