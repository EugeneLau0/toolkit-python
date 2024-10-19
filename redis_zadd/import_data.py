import redis

# 设置Redis连接的主机和端口
redis_host = 'localhost'
redis_port = 6379

# 创建Redis连接对象
redis_connect = redis.Redis(host=redis_host, port=redis_port)


# 定义生成值的函数，根据索引生成字典
def generate_value(index):
    return {'player-' + str(index): index}  # 返回一个字典，键为'goods_'加索引，值为索引


# 循环从1到1000001，生成数据并写入Redis的有序集合
for i in range(1, 1000001):
    value = generate_value(i)  # 生成当前索引的值
    redis_connect.zadd('player_board', value)

# 打印完成信息
print('写入数据完成！')
