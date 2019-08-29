from flask import Flask, g
from db import RedisClient

app = Flask(__name__)


def get_conn():
    if not hasattr(g, "redis"):
        g.redis = RedisClient()
    return g.redis


@app.route("/")
def index():
    return "<h2>欢迎使用代理ip池检测系统</h2>"


@app.route("/random")
def get_proxy():
    """
    获取随机代理的接口
    :return: 随机代理ip
    """
    coon = get_conn()
    return coon.random()


@app.route("/count")
def get_conuts():
    """
    获取代理ip池总量
    :return: 总数量
    """
    coon = get_conn()
    return str(coon.count())


if __name__ == '__main__':
    app.run()
