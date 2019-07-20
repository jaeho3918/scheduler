import pymysql

conn = pymysql.connect(host='112.172.237.233:8505', user='comm', password='gana2939!', db='gana', charset='utf8mb4')

curs = conn.cursor()