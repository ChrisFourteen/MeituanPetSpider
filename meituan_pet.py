# -*- coding: UTF-8 -*-
# import gevent.monkey
#
# gevent.monkey.patch_all()
import requests
import time
from lxml import etree
import pymysql
import logging
import json
from gevent.pool import Pool
from queue import Queue
from get_proxy import get_proxy_ip
import random

"""
美团宠物店信息
"""


def get_shop(r):
    # print(r.content.decode('utf-8'))
    tree = etree.HTML(r.content)
    hr_li = tree.xpath('//div[@class="common-list-main"]/div/a/@href')
    shop_li = []
    for hr in hr_li:
        if 'chongwu' in hr:
            shop = 'https:' + hr
            shop_li.append(shop)
    return shop_li


def get_data(r, city):
    try:
        tree = etree.HTML(r.content)
        name = tree.xpath('//h1/text()')[0]
        tel = tree.xpath('//div[@class="seller-info-body"]/div[2]/span[2]/text()')[0]
        address = tree.xpath('//div[@class="seller-info-body"]/div[1]/a/span/text()')[0]
        return {
            'city': city,
            'name': name,
            'tel': tel,
            'address': address
        }
    except Exception as e:
        print(e)
        print('获取失败')


def sess_get(url, sess):
    num = 0
    r = None
    while num < 5:
        try:
            proxy = get_proxy_ip()
            # proxy_li = get_proxy_ip()
            # proxy = proxy_li[random.randint(1, len(proxy_li))]
            # print(proxy)
            sess.proxies = proxy
            r = sess.get(url, timeout=20)
        except Exception as e:
            # print(e)
            print('代理失效')
        if r:
            break
        num += 1
    return r


# http://i.meituan.com/index/changecity
# //div[@class="alphabet-city-area"]/div/span/a/@href
def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    sess = requests.Session()
    sess.headers = headers
    city_url = 'https://www.meituan.com/changecity/'
    response = sess.get(city_url)
    city_tree = etree.HTML(response.content)
    a_li = city_tree.xpath('//div[@class="alphabet-city-area"]/div/span/a')
    city_di = {}
    for a in a_li:
        h = 'https:' + a.xpath('./@href')[0] + '/chongwu'
        ci = a.xpath('./text()')[0]
        city_di[ci] = h
    # print(city_di)
    for city, list_u in city_di.items():
        num = 1
        while True:
            parsr_url = list_u + '/pn%d/' % num
            # print(parsr_url)
            # proxy = get_proxy()
            resp = sess_get(parsr_url, sess)
            if not resp:
                break
            # print(resp.content.decode('utf-8'))
            if '没有符合条件的商家' in resp.content.decode('utf-8'):
                break
            shop_li = get_shop(resp)
            # print(shop_li)
            for shop in shop_li:
                # print(shop)
                r = sess_get(shop, sess)
                if r:
                    # print(shop)
                    data = get_data(r, city)
                    print(data)
                    # time.sleep(0.1)
                else:
                    data = None
            num += 1


if __name__ == '__main__':
    main()
    # print(get_proxy_ip())
