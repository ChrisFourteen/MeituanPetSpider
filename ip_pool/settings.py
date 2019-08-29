# redis数据库的相关配置
# 数据库地址
REDIS_HOST = "127.0.0.1"
# 端口号
REDIS_PORT = 6379
# 密码  没有密码 默认为None值
REDIS_PASSWORD = None
# 抓取下来之后 保存的默认分数
DEFAULT_SCORE = 10
# 可用的分数
MAX_SCORE = 100
# 最小分数 小于这个分数 直接删除
MIN_SCORE = 0
# 存储代理 IP 的redis key
REDIS_KEY = "proxies"


# 测试模块中 批量测试的数量
BATCH_TEST_SIZE = 5

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 是否调用的开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True