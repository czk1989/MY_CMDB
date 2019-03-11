#_*_coding:utf-8_*_

from MY_CMDB import settings
import redis

def redis_conn():
    #print(django_settings.REDIS_CONN)
    pool = redis.ConnectionPool(host=settings.REDIS_CONN['HOST'],
                                port=settings.REDIS_CONN['PORT'],
                                db=settings.REDIS_CONN['DB'],
                                password=settings.REDIS_CONN['PASSWORD'])
    r = redis.Redis(connection_pool=pool)
    return  r