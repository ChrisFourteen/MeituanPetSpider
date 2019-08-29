# -*- coding: UTF-8 -*-
import requests
import json
import time
from lxml import etree
import pymysql


def insert_data(name, address, tel):
    """
    向mysql插入数据记录
    :return:
    """
    address = '"' + address + '"'
    tel = '"' + tel + '"'
    name = '"' + name + '"'
    db = pymysql.connect('localhost', 'root', 'mysql', 'meituan')
    cursor = db.cursor()
    sql = """insert into Meituan_Pet values(default,%s,%s,%s);""" % (name, address, tel)
    # print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print("插入成功")
        time.sleep(0.01)
    except Exception as e:
        print(e)
        db.rollback()
        print("插入失败")


s_u = 'http://i.meituan.com/poi/{}'
u = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/{}?uuid=035ea30ae843482ead5c.1564282547.1.0.0&userid=-1&limit=1000&offset=0&cateId=-1&q=宠物'
# r = requests.get(u)
# ret = json.loads(r.content.decode('utf-8'))
# # with open('tesst.json', 'w')as f:
# #     f.write(r.content.decode('utf-8'))
# print(len(ret['data']['searchResult']))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
shop_id = []
for i in range(1, 1000):
    url = u.format(str(i))
    r = requests.get(url)
    time.sleep(0.01)
    ret = json.loads(r.text)
    shop_li = ret['data']['searchResult']
    for shop in shop_li:
        id = str(shop['id'])
        shop_id.append(id)
    print(str(i))
shop_id_li = list(set(shop_id))
print(len(shop_id_li))

for id in shop_id_li:
    try:
        url = s_u.format(id)
        response = requests.get(url, headers=headers)
        tree = etree.HTML(response.text)
        name = tree.xpath('//dd[@class="cont"]//h1/text()')[0]
        address = tree.xpath('//div[@class="poi-address"]/text()')[0]
        tel = tree.xpath('//a[@class="react poi-info-phone"]/@data-tele')[0]
        insert_data(name, address, tel)
    except Exception as e:
        print(e)
    # shop_info = {
    #     'name': name,
    #     'address': address,
    #     'tel': tel
    # }
    time.sleep(0.01)
    # print(shop_info)
