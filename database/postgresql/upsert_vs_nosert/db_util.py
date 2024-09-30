import yaml
import psycopg2


def create_db_connection(config):
    # 创建数据库连接
    connection = psycopg2.connect(
        dbname=config['database_name'],
        user=config['username'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        options=f"-c search_path={config['schema']}"  # 添加schema
    )
    return connection


def read_sql_script():
    with open('test_table.sql', 'r') as file:
        return file.read()


def execute_sql(config=None, connection=None, sql=None):
    if connection is None:
        if config is None:
            raise ValueError("连接对象为空时，config不能也为空")
        connection = create_db_connection(config)
    if sql is None:
        raise ValueError("执行的sql不能为空")
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
        connection.close()


def execute_sql_with_params(config=None, connection=None, sql=None, inventory_items: list = list):
    if connection is None:
        if config is None:
            raise ValueError("连接对象为空时，config不能也为空")
        connection = create_db_connection(config)
    if sql is None:
        raise ValueError("执行的sql不能为空")
    if inventory_items is None:
        raise ValueError("执行的参数不能为空")
    data = [(item.materialid, item.stockid, item.spaceid, item.auxpropid, item.batchno, item.kfdata,
             item.validate, item.qty, item.validqty) for item in inventory_items]

    with connection.cursor() as cursor:
        # 使用executemany方法执行批量插入
        cursor.executemany(sql, data)
        connection.commit()
        connection.close()


def init(config):
    connection = create_db_connection(config)
    create_table_sql = read_sql_script()
    execute_sql(connection=connection, sql=create_table_sql)
