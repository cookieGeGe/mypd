from json import dumps

from main.redishelper import RedisHelper

obj = RedisHelper()
for i in range(5):
    a = {'hello': 'how are you?'}
    obj.public(dumps(a))
