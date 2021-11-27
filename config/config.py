import os


class Config:

    GROUP_NAME = 'ubank'
    PROJECT_NAME = 'wealth_city_county'

    SCHEDULED_DICT = {
        'spider_interval': int(os.getenv('spider_INTERVAL', 720)),             # 定时爬取时间间隔720分钟
        'master_interval': int(os.getenv('master_INTERVAL', 1)),
    }
    MASTER_CRAWL_PER_TIME = 1000

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # DATA_DIR = os.path.join(BASE_DIR, 'data')
    # os.makedirs(DATA_DIR, exist_ok=True)
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    os.makedirs(LOG_DIR, exist_ok=True)

    TIMEZONE = 'Asia/Shanghai'
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

    HOST_LOCAL = '192.168.3.110'
    HOST_REMOTE = '192.168.3.110'

    MYSQL_DICT = dict(
        ENDPOINT=os.getenv('MYSQL_ENDPOINT', HOST_LOCAL),
        PORT=int(os.getenv('MYSQL_PORT', 3306)),
        DB=os.getenv('MYSQL_DB', GROUP_NAME),
        USER=os.getenv('MYSQL_USERNAME', 'root'),
        PASSWORD=os.getenv('MYSQL_PASSWORD', '123456'),
    )

    MONGO_DICT = dict(
        ENDPOINT=os.getenv('MONGO_ENDPOINT', HOST_LOCAL),
        PORT=int(os.getenv('MONGO_PORT', 27017)),
        DB=os.getenv('MONGO_DB', GROUP_NAME),
        USERNAME=os.getenv('MONGO_USERNAME', 'root'),
        PASSWORD=os.getenv('MONGO_PASSWORD', '123456'),
    )

    # Redis数据库分类：
    # 数据库0：备用
    # 数据库1：保存代理IP
    # 数据库2：保存爬取成功或失败的urls
    # 数据库3：保存爬取成功或失败的urls
    REDIS_DICT = dict(
        ENDPOINT=os.getenv('REDIS_ENDPOINT', HOST_LOCAL),
        PORT=int(os.getenv('REDIS_PORT', 6379)),
        DB=int(os.getenv('REDIS_DB', 3)),
        PASSWORD=os.getenv('REDIS_PASSWORD', '123456')
    )

    FILE_SUFFIX = ['.pdf', '.doc', '.docx']

    HTML_TYPE = {
        'outline': '理财列表',
        'manual': '产品说明书',
        'notice_issue': '产品发行公告',
        'notice_start': '产品成立公告',
        'notice_end': '产品终止公告',
    }

