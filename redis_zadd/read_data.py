import time
import redis

# 设置Redis连接的主机和端口
redis_host = 'localhost'
redis_port = 6379

# 创建Redis连接对象
redis_connect = redis.Redis(host=redis_host, port=redis_port)

# 定义起始和结束索引，以及迭代次数
start_index = 0
end_index = 9
num_iterations = 100

# 初始化总时间
total_time = 0

# 进行指定次数的迭代
for _ in range(num_iterations):
    start_time = time.time()  # 记录开始时间
    # 从Redis中获取指定范围的有序集合数据
    result = redis_connect.zrange('player_board', start_index, end_index, withscores=True)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算经过的时间
    total_time += elapsed_time  # 累加总时间

    # 打印结果和经过的时间
    print('Result: ', result)
    print('Elapsed time: ', elapsed_time, 'seconds')

# 计算平均时间
average_time = total_time / num_iterations
# 打印平均时间
print('Average time: ', average_time * 1000, 'ms')
