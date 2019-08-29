from db import RedisClient
from crawler import Crawler


class Getter(object):

    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def run(self):
        print("开始抓取代理ip")

        ips_list = self.crawler.run()
        for ip in ips_list:
            self.redis.add(ip)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
