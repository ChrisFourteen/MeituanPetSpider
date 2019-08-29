import requests
from db import RedisClient
from settings import BATCH_TEST_SIZE


class Tester(object):

    def __init__(self):
        self.redis = RedisClient()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.test_url = ""

    def parse_url(self, proxy):

        print("即将开始测试代理： ", proxy)

        if proxy.split(":")[0] == "http":
            proxies = {"http": proxy}
            self.test_url = "http://www.xinhuanet.com"
        else:
            proxies = {"https": proxy}
            self.test_url = "https://www.baidu.com"

        try:
            print(self.test_url)
            response = requests.get(self.test_url, proxies=proxies, headers=self.headers, timeout=3)

            if response.status_code == 200:
                self.redis.max(proxy)
                print("发现可用代理： ", proxy)
            else:
                self.redis.decrease(proxy)
                print("响应状态玛不合法： ", response.status_code, " proxy: ", proxy)
        except Exception as e:
            self.redis.decrease(proxy)
            print("请求发生错误： ", e, " proxy: ", proxy)

    def run(self):
        print("开始测试代理ip......")
        count = self.redis.count()
        print("当前剩余 ", count, " 个代理")
        for i in range(0, count, BATCH_TEST_SIZE):
            start = i
            stop = min(i + BATCH_TEST_SIZE, count)
            print("正在测试第 ", start + 1, " - ", stop, "个代理")

            test_proxies = self.redis.batch(start, stop)

            for proxy in test_proxies:
                self.parse_url(proxy)


if __name__ == '__main__':
    tester = Tester()
    tester.run()


