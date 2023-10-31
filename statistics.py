# 姓名：郭紫照
from settings import *
import redis

redis_1 = redis.StrictRedis(
    host=REDIS['host'],
    port=REDIS['port'],
    db=REDIS['db'],
    password=REDIS['password'],
)

berause1 = redis_1.smembers(REDIS['manta_comp'])
data_list = []
for j in berause1:
    auto = j.decode('utf-8')
    data = int(auto.split(',')[-1])
    data_list.append(data)

sum = 0
for i in data_list:
    sum += i
print(sum)
