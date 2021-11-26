import aioredis
import random
from database.db_settings import Settings
from functools import wraps
from config import singleton, CONFIG
import asyncio

try:
    from ujson import dumps as json_dumps
    from ujson import loads as json_loads
except:
    from json import dumps as json_dumps
    from json import loads as json_loads


REDISDB = Settings.redisdb_config


# 使用装饰器dec_connector：数据库redis连接 使用，检查数据库是否有连接上，如果未连接，则进行连接
def dec_connector(func):
    # 装饰器 作用于函数 func
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self._client_conn is None:
            self._client_conn = await self._connector()
        return await func(self, *args, **kwargs)
    return wrapper


@singleton
class RedisDatabase(object):

    _db = {}
    _client_conn = None

    def __init__(
            self,
            host=REDISDB['host'],
            port=REDISDB['port'],
            db=REDISDB['db'],
            password=REDISDB['password'],
            name=CONFIG.GROUP_NAME,
            **kwargs
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.name = name

    @dec_connector
    async def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """
        def gen_keys(keys):
            all_keys = []
            for key in keys:
                if isinstance(key, list):
                    all_keys += gen_keys(keys=key)
                else:
                    all_keys.append(key)
            return all_keys

        all_keys = gen_keys(keys)
        for key in all_keys:
            await self._client_conn.hdel(key=self.name, field=key)

    @dec_connector
    async def delete_one(self, field, **kwargs):
        result = await self.exists(field=field)
        if result:
            await self._client_conn.hdel(key=self.name, field=field)

    @dec_connector
    async def exists(self, field, **kwargs):
        """
        Return a boolean indicating whether key field exists
        """
        return await self._client_conn.hexists(key=self.name, field=field)

    @dec_connector
    async def get(self, field, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        return await self._client_conn.hget(self.name, field=field)

    @dec_connector
    async def get_all(self, default=None, **kwargs):
        """
        Return all values
        """
        try:
            res = await self._client_conn.hgetall(self.name)
            all_dict = {key.decode('utf-8'): json_loads(value.decode('utf-8')) for key, value in res.items()}
        except Exception as e:
            all_dict = default
        return all_dict

    @dec_connector
    async def get_random(self, default=None, **kwargs):
        """
        Return a random value
        """
        all_dict = await self.get_all()
        if all_dict:
            key = random.choice(list(all_dict.keys()))
            return {key: all_dict[key]}
        else:
            return default

    @dec_connector
    async def get_randoms(self, num=100, **kwargs):
        """
        Return a random list
        """
        list_random = []
        keys_random = set()
        all_dict = await self.get_all()
        if all_dict:
            if len(all_dict) > num:
                while len(keys_random) < num:
                    key = random.choice(list(all_dict.keys()))
                    keys_random.add(key)
                for key in keys_random:
                    list_random.append(all_dict[key])
            else:
                list_random = all_dict.values()
        return list_random


    @dec_connector
    async def insert(self, field, value={}, **kwargs):
        """
        insert the value, 如不存在，则新增
        """
        isexist = await self.exists(field)
        if not isexist:
            if isinstance(value, (list, dict)):
                value = json_dumps(value)
            return await self._client_conn.hset(key=self.name, field=field, value=value)

    @dec_connector
    async def update_one(self, field, value={}, **kwargs):
        """
        update the value  如已经存在，则更新；如不存在，则当中新增插入；
        新增，返回1
        更新，返回0
        """
        if isinstance(value, (list, dict)):
            value = json_dumps(value)
        return await self._client_conn.hset(key=self.name, field=field, value=value)

    async def _db_client(self, db=None):
        client = await aioredis.create_redis_pool(
            'redis://{host}:{port}/{cur_db}'.format(host=self.host, port=self.port, cur_db=db),
            password=self.password,
            minsize=5,
            maxsize=10
        )
        return client

    async def _connector(self, db=None):
        if db is None:
            db = self.db
        if db not in self._db:
            self._db[db] = self._client_conn = await self._db_client(db)
        return self._db[db]


def test():
    import asyncio
    redis_client = RedisDatabase()

    print(asyncio.get_event_loop().run_until_complete(redis_client.insert(field='127.0.0.1:8001', value={'a': 1, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.insert(field='127.0.0.1:8002', value={'a': 2, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.insert(field='127.0.0.1:8003', value={'a': 3, 'b': 2})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
    print('--------------------------------------------------------------------')

    print(asyncio.get_event_loop().run_until_complete(redis_client.insert(field='127.0.0.1:8002', value={'a': 22, 'b': 22})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_random()))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get(field='127.0.0.1:8003')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
    print('--------------------------------------------------------------------')

    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.delete('127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.exists(field='127.0.0.1:8001')))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))
    print('--------------------------------------------------------------------')

    print(asyncio.get_event_loop().run_until_complete(redis_client.update_one(field='127.0.0.1:8002', value={'a': 222, 'b': 222})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.update_one(field='127.0.0.1:8003', value={'a': 33, 'b': 33})))
    print(asyncio.get_event_loop().run_until_complete(redis_client.get_all()))


if __name__ == '__main__':
    test()

