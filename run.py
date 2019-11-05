# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     run
    Description:  主函数
    Author:       瓦都尅
    Date:         2019/11/2
-----------------------------------
'''
import click

from manager.proxy_schedule import run_schedule
from app.api import run_web
from conf.setting import LOGO

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def main():
    """PrxoyPool主函数"""


@main.command(name='schedule')
def schedule():
    """启动代理管理程序"""
    click.echo(LOGO)
    run_schedule()


@main.command(name='webserver')
def web():
    """启动web服务"""
    click.echo(LOGO)
    run_web()


if __name__ == '__main__':
    main()
