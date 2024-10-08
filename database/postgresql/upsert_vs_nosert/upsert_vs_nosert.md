参数文件：`upsert_vs_nosert.param`
参数格式：

```yaml
database:
  type: postgresql
  host: 172.20.184.26
  port: 5432
  username: jdy
  password: Jdy#830c73f3fb22
  database_name: jdyapp_shard1
  schema: kd_1661935242637216102
  connection_timeout: 30
  sslmode: require
# 同步执行
sync: true
batch_record: 200
concurrent_count: 10
excel_output: true

```