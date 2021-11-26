from config import CONFIG


class Settings:

    mysqldb_config = {
        'host': CONFIG.MYSQL_DICT['ENDPOINT'],
        'port': CONFIG.MYSQL_DICT['PORT'],
        'db': CONFIG.MYSQL_DICT['DB'],
        'user': CONFIG.MYSQL_DICT['USER'],
        'password': CONFIG.MYSQL_DICT['PASSWORD'],
    }

    redisdb_config = {
        'host': CONFIG.REDIS_DICT['ENDPOINT'],
        'port': CONFIG.REDIS_DICT['PORT'],
        'db': CONFIG.REDIS_DICT['DB'],
        'password': CONFIG.REDIS_DICT['PASSWORD'],
    }

    mongodb_config = {
        'host': CONFIG.MONGO_DICT['ENDPOINT'],
        'port': CONFIG.MONGO_DICT['PORT'],
        'db': CONFIG.MONGO_DICT['DB'],
        'username': CONFIG.MONGO_DICT['USERNAME'],
        'password': CONFIG.MONGO_DICT['PASSWORD'],
    }

    # 理财爬取 步骤
    # 第一步 Spider爬取，获取各银行网站上的原始信息 【MongoDB数据库：mywealth_spider】
    # 1、原始的理财列表信息【对应表名：各银行中文名称】
    # 2、产品说明书PDF或DOC文件链接【对应表名：MANUAL_URL】
    # 3、产品说明书内容【对应表名：MANUAL】，主要是保存网页类型的说明书，即从网页上提取出产品说明书的部分，然后保存为html格式的文件，放入数据库中

    # 第二步 对爬取的内容进行归档整理, 【MongoDB数据库：mywealth_formatter】
    # 1、将各银行的理财列表信息，统一转换为Wealth类 进行保存【对应表名：WEALTH_OUTLINE】
    # 2、WEALTH_OUTLINE各表、MANUAL_URL表、MANUAL表 上传至 “下载器”

    # 第三步 “下载器”【MongoDB数据库：mywealth_downloader】
    # 1、按照MANUAL_URL中的链接，下载PDF或DOC或HTML, 将内容保存至MANUAL_CONTENT表
    # 2、将WEALTH_OUTLINE各表、MANUAL_URL表、MANUAL表 传递给 “提取器”

    # 第四步 “提取器”【MongoDB数据库：mywealth_cleaner】
    # 1、将PDF等文件中的内容提取出来，保存为统一的WEALTH类【对应表名：WEALTH】
    # 2、将WEALTH表、MANUAL表上传至 服务器MongoDB和ElasticSearch数据库中，供前端搜索查询使用

    # 第五步 “分析器” 针对WEALTH表的数据，作数据分析

    # 第六步 最终展示给前端的内容，都保存在【MongoDB数据库：myworld】中

