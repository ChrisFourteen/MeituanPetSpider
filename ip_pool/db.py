import redis
from random import choice
from error import PoolEmptyError

from settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,DEFAULT_SCORE,MAX_SCORE,MIN_SCORE,REDIS_KEY


class RedisClient():

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化 连接redis数据库
        :param host: redis地址
        :param port: redis端口号
        :param password: redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port,password=password,decode_responses=True)

    def add(self, proxy, score=DEFAULT_SCORE):
        """
        添加代理 给代理设置默认的分数10
        :param proxy: 代理
        :param score: 分数
        :return: 添加的结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        返回获取有效代理，先尝试获取最高分的代理，如果不存在，按照分数进行排序 获取， 否则异常
        :return: 随机的代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理分数 -1 分, 小于最小值则删除
        :param proxy: 代理
        :return: 修改之后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print("代理：", proxy, " 当前的分数: ", score," 减 1 ")
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("代理：", proxy, " 当前的分数: ", score, " 移除")
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理ip是否存在
        :param proxy: 代理ip
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理ip
        :return: 设置结果
        """
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理的数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理的列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.count()
    print(result)














































