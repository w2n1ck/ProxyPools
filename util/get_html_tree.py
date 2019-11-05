# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     get_html_tree
    Description:  XML处理HTML
    Author:       瓦都尅
    Date:         2019/10/30
-----------------------------------
'''
from lxml import etree
from .web_requests import webRequest

def getHtmlTree(url, **kwargs):

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    wr = webRequest()
    html = wr.get(url=url, header=header).content
    return etree.HTML(html)


# getHtmlTree('http://www.baidu.com/')