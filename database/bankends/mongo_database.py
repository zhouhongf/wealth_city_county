from pymongo import MongoClient, collection
from config import singleton, CONFIG
from database.db_settings import Settings
import bson.binary
from gridfs import *
import time

MONGODB = Settings.mongodb_config


@singleton
class MongoDatabase:

    # ===================================初始化数据库并建立连接=========================================
    # 数据量一多，频繁的增删查改，将极大的占用硬盘空间，
    # 如果是大数据储存，建议使用MySQL

    def client(self):
        mongo = MongoClient(
            host=MONGODB['host'] if MONGODB['host'] else 'localhost',
            port=MONGODB['port'] if MONGODB['port'] else 27017,
            username=MONGODB['username'] if MONGODB['username'] else '',
            password=MONGODB['password'],
        )
        return mongo

    def db(self):
        return self.client()[MONGODB['db']]

    @staticmethod
    def upsert(collec: collection, condition: dict, data: dict):
        result = collec.find_one(condition)
        if result:
            collec.update_one(condition, {'$set': data})
            print('MONGO数据库《%s》中upsert更新: %s' % (collec.name, condition))
            return None
        else:
            collec.insert_one(data)
            print('MONGO数据库《%s》中upsert新增: %s' % (collec.name, condition))
            return condition

    @staticmethod
    def do_insert_one(collec: collection, condition: dict, data: dict):
        result = collec.find_one(condition)
        if result:
            print('MONGO数据库《%s》中do_insert_one已存在: %s' % (collec.name, condition))
            return None
        else:
            collec.insert_one(data)
            print('MONGO数据库《%s》中do_insert_one新增: %s' % (collec.name, condition))
            return condition


def backup_database():
    time_start = time.perf_counter()
    print('===================================运行MongoDB备份: %s=========================================' % time_start)
    mongo = MongoDatabase()
    mongo_db = mongo.db()
    collection_client_url = mongo_db['MANUAL_URL']

    mongo_server = MongoClient(host=CONFIG.HOST_REMOTE, port=27017, username=MONGODB['username'], password=MONGODB['password'])
    try:
        mongo_db_server = mongo_server[MONGODB['db']]
        collection_server_url = mongo_db_server['MANUAL_URL']

        client_urls = collection_client_url.find({'status': 'undo'})
        if client_urls.count() > 0:
            for data in client_urls:
                condition = {'_id': data['_id']}
                result = collection_server_url.find_one(condition)
                if not result:
                    done = collection_server_url.insert_one(data)
                    if done:
                        data['status'] = 'uploaded'
                        collection_client_url.update_one(condition, {'$set': data})
        else:
            print('MANUAL_URL数据库中没有还没有上传到server的记录')
    except:
        print('===================================未能连接远程SERVER=======================================')

    time_end = time.perf_counter()
    print('===================================完成MongoDB备份: %s, 用时: %s=========================================' % (time_end, (time_end - time_start)))




