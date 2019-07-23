import pymysql

def insert(input_array):
    conn = pymysql.connect(host='112.172.237.233', port = 8505, user='memo_all', password='zn@(h21^v75$0-234h', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "INSERT : READY")

    result = []

    sql = "INSERT INTO `memo`(`stat`, `contents`, `wirteday`, `completeday`, `complete`, `delete`, `realday`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(*input_array)

    print('query :', sql)

    print(ord('`'))

    curs.execute(sql)
    conn.commit()
    curs.close()
    conn.close()


def select():
    conn = pymysql.connect(host='112.172.237.233',port = 8505, user='memo_all', password='zn@(h21^v75$0-234h', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "SELECT : READY")

    result = []

    sql = "SELECT * " \
          "from memo " \
          "WHERE id = {0} ORDER BY id DESC".format(1)
    print('query :', sql)
    curs.execute(sql)

    rows = curs.fetchall()

    curs.close()
    conn.close()

    return rows

def update(idx,contents):
    conn = pymysql.connect(host='112.172.237.233',port = 8505, user='memo_all', password='zn@(h21^v75$0-234h', db='gana', charset='utf8mb4')
    curs = conn.cursor()
    print(curs, "UPDATE : READY")

    column_table = ["`stat`", "`contents`", "`wirteday`", "`completeday`", "`complete`", "`delete`", "`realday`"]

    set_contents = ["`{}`={}".format(column_table[int(i[0])], i[1]) for i in contents]

    result = []

    sql_part1 = "UPDATE memo SET"
    sql_part2 = "{}={}"*len(set_contents)
    sql_part2.format(*set_contents)
    sql_part3 = "WHERE Id={1} %".format(int(idx))

    sql = sql_part1, sql_part2, sql_part3

    print('query :', sql)

    curs.execute(sql)

    conn.commit()
    curs.close()
    conn.close()



# select()
insert([1,
       '테스트ㅇㅂㅇㅂㅇ',
       "MM월 dd일 dddd  ap hh:mm:ss",
       "MM월 dd일 dddd  ap hh:mm:ss",
       0,
       0,
       "MM월 dd일 dddd  ap hh:mm:ss"])
