# -*- coding: utf-8 -*-
'''
-----------------------------------
    FileName:     get_free_proxyip
    Description:  代理抓取函数
    Author:       瓦都尅
    Date:         2019/10/30
-----------------------------------
'''
import re
import time

from util.get_html_tree import getHtmlTree
from util.web_requests import webRequest


class GetFreeProxy(object):

    @staticmethod
    def freeProxy01():
        """
        无忧代理 http://www.data5u.com/
        """
        url_list = [
            'http://www.data5u.com/',
        ]
        key = 'ABCDEFGHIZ'
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    ip = ul.xpath('./span[1]/li/text()')[0]
                    port = ul.xpath('./span[2]/li/text()')[0]
                    # classname = classnames.split(' ')[1]
                    # port_sum = 0
                    # for c in classname:
                    #     port_sum *= 10
                    #     port_sum += key.index(c)
                    # port = port_sum >> 3
                    yield '{}:{}'.format(ip, port)
                except Exception as e:
                    print(e)


    @staticmethod
    def freeProxy02(count=50):
        """
        代理66 http://www.66ip.cn/
        """
        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&s"
            "tart=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"
        ]
        for url in urls:
            wq = webRequest()
            ip = wq.get(url.format(count)).text

            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", ip)
            for ip in ips:
                yield ip.strip()


    @staticmethod
    def freeProxy03(page_count=1):
        """
        西刺代理 http://www.xicidaili.com
        """
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    @staticmethod
    def freeProxy04():
            """
            guobanjia http://www.goubanjia.com/
            """
            url = "http://www.goubanjia.com/"
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            xpath_str = """.//*[not(contains(@style, 'display: none'))
                                            and not(contains(@style, 'display:none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
            for each_proxy in proxy_list:
                try:
                    ip_addr = ''.join(each_proxy.xpath(xpath_str))
                    port = 0
                    for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                              "/attribute::class")[0]. \
                            replace("port ", ""):
                        port *= 10
                        port += (ord(_) - ord('A'))
                    port /= 8

                    yield '{}:{}'.format(ip_addr, int(port))
                except Exception as e:
                    pass

    @staticmethod
    def freeProxy05():
        """
        快代理 https://www.kuaidaili.com
        """

        url_list = [
                'https://www.kuaidaili.com/free/inha/',
                'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            time.sleep(2)
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])


    @staticmethod
    def freeProxy06():
        """
        云代理 http://www.ip3366.net/free/
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"]
        wq = webRequest()
        for url in urls:
            r = wq.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)


    @staticmethod
    def freeProxy07():
        """
        IP海 http://www.iphai.com/free/ng
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        wq = webRequest()
        for url in urls:
            r = wq.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)


    @staticmethod
    def freeProxy08(page_count=5):
        """
        全球免费代理IP库 http://ip.jiangxianli.com/?page=
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]


    @staticmethod
    def freeProxy09(max_page=5):
        """
        齐云代理 http://www.qydaili.com/free/?action=china&page=1
        """
        base_url = 'http://www.qydaili.com/free/?action=china&page={}'
        wq = webRequest()
        for page in range(1, max_page + 1):
            r = wq.get(base_url.format(str(page)))
            proxies = re.findall(r'<td.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td.*?>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


    @staticmethod
    def freeProxy10(max_page=5):
        """
        89免费代理 http://www.89ip.cn/index.html
        """
        base_url = 'http://www.89ip.cn/index_{}.html'
        wq = webRequest()
        for page in range(1, max_page + 1):
            r = wq.get(base_url.format(str(page)))
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    from .check_proxy import CheckProxy
    CheckProxy.checkAllGetProxyFunc()