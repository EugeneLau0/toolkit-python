import asyncio

import yaml
import business_helper as business

import db_util as db


def load_db_config(file_path='upsert_vs_nosert.param'):
    # 读取YAML配置文件
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def init_db(config):
    db.init(config)
    # 清空表数据
    db.execute_sql(config=config, sql='truncate table test_table;')


async def run_async_operations(items):
    tasks = []
    # 并发更新
    for i in range(concurrent_count):  # 修改为10次执行
        tasks.append(asyncio.to_thread(business.insert_inventory_item, config, items))  # 添加任务到列表
    insert_result = await asyncio.gather(*tasks)

    tasks = []
    # 并发更新
    for i in range(concurrent_count):  # 修改为10次执行
        tasks.append(asyncio.to_thread(business.upsert_inventory_item, config, items))  # 添加任务到列表
    upsert_result = await asyncio.gather(*tasks)  # 等待所有任务完成

    for i in range(concurrent_count):
        if excel_output:
            print(
                f'{i + 1}\t{insert_result[i]}\t{upsert_result[i]}\t{-1 * round(insert_result[i] - upsert_result[i], 2)}')
        else:
            print(f'第{i + 1}次insert&update耗时：{insert_result[i]}，upsert耗时：{upsert_result[i]}，'
                  f'前者比后者快：{-1 * round(insert_result[i] - upsert_result[i], 2)}秒')


def run_sync_operations(items):
    for i in range(concurrent_count):
        first_time = business.insert_inventory_item(config, items)
        second_time = business.upsert_inventory_item(config, items)
        if excel_output:
            print(f'{i + 1}\t{first_time}\t{second_time}\t{-1 * round(first_time - second_time, 2)}')
        else:
            print(f'第{i + 1}次insert&update耗时：{first_time}，upsert耗时：{second_time}，'
                  f'前者比后者快：{-1 * round(first_time - second_time, 2)}秒')


params = load_db_config()
config = params['database']
concurrent_count = params['concurrent_count']
excel_output = params['excel_output']

if __name__ == '__main__':
    init_db(config)
    items = list()
    count = params['batch_record']
    for i in range(1, count + 1):
        items.append(business.create_inventory_item(i))
    if params['sync']:
        print(f'批量更新【{count}】条记录，开始交叉冲突更新：')
        run_sync_operations(items)
    else:
        print(f'批量更新【{count}】条记录，开始异步更新：')
        asyncio.run(run_async_operations(items))
    print('更新完成！')
