# ProxyPools
> 之前做的代理池，最近有需要，又用了起来，但是，emmm... 所以重构了下，可用性还是很高的。

临时API：http://94.191.42.63:9090/random

#### 源代码

**app:** web服务

**conf:** 全局配置

**db:** redis数据操作

**log:** 日志文件目录

**manager:** 代理调度管理

**proxy:** 代理抓取与格式化

**util:** 日志，网页请求，网页处理

**run.py:** 主函数

```
├── app
│   ├── __init__.py
│   └── api.py
├── conf
│   ├── __init__.py
│   └── setting.py
├── db
│   ├── __init__.py
│   ├── db.py
│   └── redis_client.py
├── env
├── log
│   └── test.log
├── manager
│   ├── __init__.py
│   ├── check_available_proxy.py
│   ├── check_init_proxy.py
│   ├── proxy_manager.py
│   └── proxy_schedule.py
├── proxy
│   ├── __init__.py
│   ├── check_proxy.py
│   ├── get_free_proxyip.py
│   └── proxy_info.py
├── requirements.txt
├── run.py
└── util
    ├── __init__.py
    ├── get_html_tree.py
    ├── log_handler.py
    ├── test.py
    └── web_requests.py
```

#### 使用

##### 1、启动任务

![](http://blog.w2n1ck.com/schedule.png)

![](http://blog.w2n1ck.com/schedule_pass.png)

![](http://blog.w2n1ck.com/schedule_cron.png)

##### 2、启动webserver

![](http://blog.w2n1ck.com/webserver.png)

> 源代码公众号回复“代理” 获取

### 优化

#### 1. 延迟计算

你想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。 但是一旦被访问后，你希望结果值被缓存起来，不用每次都去计算。

对应此程序的爬取代理的多个函数

```python
class LazyProperty(object):
    """
    LazyProperty https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p10_using_lazily_computed_properties.html
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
        return ['freeProxy01','freeProxy02']

# 调用
get_function = GetFunctions()
        for proxy_get in get_function.proxy_get_functions:
            try:
                for proxy in getattr(GetFreeProxy, proxy_get.strip())():
                    ...
```

#### 2. 单例模式

如果在程序运行期间，有很多地方都需要使用配置文件的内容，也就是说，很多地方都需要创建 AppConfig 对象的实例，这就导致系统中存在多个 AppConfig 的实例对象，而这样会严重浪费内存资源 。事实上，类似 AppConfig 这样的类，我们希望在程序运行期间只存在一个实例对象。 

对应此程序的数据库的操作

```python
class Singleton(type):
    """
    Singleton Metaclass http://funhacks.net/2017/01/17/singleton/
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args)
        return cls._instances[cls]

class DBclient(object, metaclass=Singleton):
    ...
```

#### 3. Webserver

Gunicorn是一个Python WSGI HTTP Server。gunicorn可以直接使用命令行gunicorn进行调用，也可以在python中构建Application进行使用。

```python
'''https://gist.github.com/KatiRG/2bdf792893bb475ae8debef87002e02c'''
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

from flask import Flask, render_template, make_response, request, Response #etc

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }
    StandaloneApplication(app, options).run()
```

#### 4. 自动返回Json响应

 API接口通常返回的是Json， 如果每个返回Json的路由都需要这样处理，那么对接口数量众多的的API来说重复工作就太多了。

```python
class MyResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)

app.response_class = MyResponse
```

#### 5. 任务调度

`APScheduler`是一个python的第三方库，用来提供python的后台程序。包含四个组件，分别是：

- triggers： 任务触发器组件，提供任务触发方式
- job stores： 任务商店组件，提供任务保存方式
- executors： 任务调度组件，提供任务调度方式
- schedulers： 任务调度组件，提供任务工作方式

```python
from apscheduler.schedulers.blocking import BlockingScheduler
import time

scheduler = BlockingScheduler()

def job():
    print(u"{}: 执行任务".format(time.asctime()))

# 添加任务并设置触发方式为3s一次
scheduler.add_job(job, 'interval', seconds=3)

scheduler.start()
```

**输出：**

```python
Sat Nov  2 17:03:33 2019: 执行任务
Sat Nov  2 17:03:36 2019: 执行任务
Sat Nov  2 17:03:39 2019: 执行任务
...
```
