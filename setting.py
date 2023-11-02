project_name = "demands:machine"
Mysql_local = {
    'host': '192.168.5.15',
    'port': 3306,
    'user': 'root',
    'password': "yuqi2018",
    'database': 'to_balalaba',
    'charset': "utf8mb4",  # 指定字符编码
}

MONGO_local = {
    'host': '192.168.5.2',
    # 'host': '127.0.0.1',
    'port': 27017,
    'db': 'demands',
    'coll': 'machine',
}

REDIS_local = {
    'host': '192.168.5.2',
    'port': 6379,
    'db': 3,
    # 已保存
    "key_du_demand": f"{project_name}:demands:du",
    # 已上传
    "key_had_demand": f"{project_name}:demands:had"
}
