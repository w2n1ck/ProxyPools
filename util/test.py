# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     test
    Description:  
    Author:       瓦都尅
    Date:         2019/10/30
-----------------------------------
'''
import re, time

import requests
from web_requests import webRequest

from get_html_tree import getHtmlTree

import click

from conf.setting import LOGO

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def cli():
    """ProxyPool """
    click.echo(LOGO)


@cli.command(name="schedule")
def schedule():
    """ 启动调度程序 """
    click.echo('hello')


if __name__ == '__main__':
    cli()