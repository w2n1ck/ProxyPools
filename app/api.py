# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     api
    Description:  代理web API
    Author:       瓦都尅
    Date:         2019/10/31
-----------------------------------
'''
from flask import Flask, jsonify
from flask import render_template
from flask import make_response
from werkzeug.wrappers import Response
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

from manager.proxy_manager import ProxyManager
from conf.setting import *

__all__ = ['app']
app = Flask(__name__)


class JsonResponse(Response):
    charset = 'utf-8'
    default_status = 200
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, (dict, list)):
            rv = jsonify(rv)

        return super(JsonResponse, cls).force_type(rv, environ)


app.response_class = JsonResponse


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])

        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


@app.route('/')
def index():
    render = render_template('index.html')
    return make_response(render)


@app.route('/random')
def get():
    """
    获取proxyAPI
    :return: 随机代理
    """
    proxy = ProxyManager().get().info_json
    return proxy if proxy else {"code": 0, "msg": "no proxy"}


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理数量
    """
    counts = ProxyManager().getCount()
    return counts if counts else {"code": 0, "msg": "no proxy"}


@app.route("/get_all")
def get_all():
    proxies = ProxyManager().getAll()
    return [_.info_dict for _ in proxies]


def run_web():
    options = {
        'bind': '{}:{}'.format(API_HOST, API_PORT),
        'workers': number_of_workers(),
        'accesslog': 'access.log',
        'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
    }
    StandaloneApplication(app, options).run()


if __name__ == '__main__':
    run_web()
