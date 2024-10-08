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

config = load_db_config()

if __name__ == '__main__':
    init_db(config)
    items = list()
    count = 200
    for i in range(1, count + 1):
        items.append(business.create_inventory_item(i))
    print('开始初始化数据：')
    for i in range(1, count + 1):
        business.insert_inventory_item(config, items)
    print('初始化数据完成！')
    print(f'批量更新【{count}】条记录，开始交叉冲突更新：')
    for i in range(1, 11):
        first_time = business.insert_inventory_item(config, items)
        second_time = business.upsert_inventory_item(config, items)
        print(
            f'第{i}次insert&update耗时：{first_time}，upsert耗时：{second_time}，前者比后者快：{-1 * round(first_time - second_time, 2)}秒')
    print('更新完成！')
