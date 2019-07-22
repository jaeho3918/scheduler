import pymysql

def insert(input_array):
    conn = pymysql.connect(host='112.172.237.233', user='comm', password='gana2939!', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "INSERT : READY")

    result = []

    sql = "INSERT INTO memo(stat, contents, wirteday, completeday, complete, delete, realday) value({0},{1},{2},{3},{4},{5},{6})".format(input_array)
    print('query :', sql)

    curs.execute(result)

    conn.commit()
    curs.close()
    conn.close()


def select():
    conn = pymysql.connect(host='112.172.237.233', user='comm', password='gana2939!', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "SELECT : READY")

    result = []

    sql = "SELECT * from memo WHERE No Like '{0}%' ORDER BY No DESC ".format()
    print('query :', sql)


    curs.close()
    conn.close()

    return result

def update():
    conn = pymysql.connect(host='112.172.237.233', user='comm', password='gana2939!', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "UPDATE : READY")
    result = []

    sql = "UPDATE memo SET commNo=%s  WHERE Id=%s % (int(no), int(Id))"
    print('query :', sql)

    curs.execute(result)

    conn.commit()
    curs.close()
    conn.close()
