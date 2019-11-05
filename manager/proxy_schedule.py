# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     proxy_schedule
    Description:  代理调度管理
    Author:       瓦都尅
    Date:         2019/11/1
-----------------------------------
'''
from apscheduler.schedulers.blocking import BlockingScheduler

from conf.setting import GETTER_CYCLE, TESTER_CYCLE
from util.log_handler import LogHandler
from .proxy_manager import ProxyManager
from .check_init_proxy import init_queue_check
from .check_available_proxy import available_queue_check


class DoFetchProxy(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)
        self.log = LogHandler('fetch_proxy')

    def main(self):
        self.log.info("***** start fetch proxy *****")
        self.fetch()
        self.log.info("***** finish fetch proxy *****")


def start_init_proxy():
    feth = DoFetchProxy()
    feth.main()
    init_queue_check()


def start_proxy_check():
    available_queue_check()


def run_schedule():
    start_init_proxy()
    start_proxy_check()

    schedule_log = LogHandler('schedule_log')
    schedule = BlockingScheduler(logger=schedule_log)

    schedule.add_job(start_init_proxy, 'interval', minutes=GETTER_CYCLE, id="start_init_proxy", name="抓取代理初始化验证")
    schedule.add_job(start_proxy_check, 'interval', minutes=TESTER_CYCLE, id="start_proxy_check", name="代理可用性定时复核")

    schedule.start()


if __name__ == '__main__':
    run_schedule()
