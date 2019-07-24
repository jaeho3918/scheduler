import pymysql

def insert(input_array):
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    #conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()

    sql = "INSERT INTO `memo`(`id`, `stat`, `contents`, `wirteday`, `completeday`, `complete`, `delete`, `realday`) " \
          "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(*input_array)

    print('INSERT 쿠어리:', sql)

    #print(ord('`'), chr(ord('`')))

    curs.execute(sql)
    conn.commit()
    curs.close()
    conn.close()


def select():
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()

    sql = "SELECT * " \
          "from memo " \
          "WHERE id = {0} ORDER BY id DESC".format(1)

    #SELECT `id`, `stat`, `contents`, `wirteday`, `completeday`, `complete`, `delete`, `realday` FROM `memo` WHERE `delete`=0 AND`complete` = 0

    print('SELECT 쿠어리:', sql, sql)

    curs.execute(sql)

    rows = curs.fetchall()

    curs.close()
    conn.close()

    return rows


def get_table():
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()

    table_sql = "SELECT `id`, `stat`, `contents`, `wirteday`, `completeday`, `complete`, `delete`, `realday` FROM `memo` " \
          "WHERE `delete`=0 AND`complete` = 0"

    # print('SELECT table 쿠어리:', table_sql)

    curs.execute(table_sql)

    table = curs.fetchall()

    complete_sql =  "SELECT `id`, `stat`, `contents`, `wirteday`, `completeday`, `complete`, `delete`, `realday` FROM `memo` " \
          "WHERE `complete` = 1 AND `delete`=0"

    # print('SELECT complete 쿠어리:', complete_sql)

    curs.execute(complete_sql)

    complete = curs.fetchall()

    curs.close()
    conn.close()

    return table, complete


def update(condition,contents):
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()

    column_table = ["`stat`", "`contents`", "`wirteday`", "`completeday`", "`complete`", "`delete`", "`realday`"]

    set_contents = ["`{}`={}".format(column_table[int(i[0])], i[1]) for i in contents]


    sql_part1 = "UPDATE memo SET"
    sql_part2 = "{}={}"*len(set_contents)
    sql_part2.format(*set_contents)
    sql_part3 = "WHERE `stat`={0} and `contents` = {1} and `wirteday` = {2} and `wirteday` = {3}".format(*condition)

    sql = sql_part1, sql_part2, sql_part3

    print('UPDATE 쿠어리:', sql)

    curs.execute(sql)

    conn.commit()
    curs.close()
    conn.close()

def get_id():
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()

    result = []

    sql = "SELECT `contents` FROM `mmt` WHERE 1"

    print('SELECT 쿠어리:', sql)

    curs.execute(sql)

    rows = curs.fetchone()

    curs.close()
    conn.close()

    return rows[0]

def increase_id():
    conn = pymysql.connect(host='192.168.0.4', port = 7704, user='memo_off', password='CiKaeUCPk9kJostF', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print("ID_UPDATE : READY")

    sql = "UPDATE `mmt` SET `contents`=`contents`+1 WHERE 1"

    print('UPDATE 쿠어리:', sql)

    curs.execute(sql)

    conn.commit()
    curs.close()
    conn.close()


