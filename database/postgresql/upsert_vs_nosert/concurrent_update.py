import asyncio
import yaml
import business_helper as business

import db_util as db


def load_db_config(file_path='upsert_vs_nosert.param'):
    # 读取YAML配置文件
    with open(file_path, 'r') as file:
        content = yaml.safe_load(file)
        return content['database']


def init_db(config):
    db.init(config)
    # 清空表数据
    db.execute_sql(config=config, sql='truncate table test_table;')


async def run_async_operations(items):
    tasks = []
    # 并发更新
    for i in range(10):  # 修改为10次执行
        tasks.append(asyncio.to_thread(business.upsert_inventory_item, config, items))  # 添加任务到列表
    await asyncio.gather(*tasks)  # 等待所有任务完成


config = load_db_config()

if __name__ == '__main__':
    init_db(config)
    items = list()
    # 初始化记录的条数
    count = 10
    for i in range(count):
        item = business.create_inventory_item(i)
        items.append(item)
    
    asyncio.run(run_async_operations(items))
