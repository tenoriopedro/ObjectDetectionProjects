## Criação da tabela "object_detect" na base de dados database_detect ## 

import mysql.connector
from datetime import datetime


DB_NAME = 'database_detect'
TABLE_NAME = 'object_detect'

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vasco123',
    database=DB_NAME
    )
cursor = connection.cursor()

cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ('
            'object_detect VARCHAR(100) NOT NULL, '
            'date_detect VARCHAR(100) NOT NULL '
            ')'
        )

def save_data_sql(list):

    object_detect = list[0]
    date_detect = list[1]


    database = get_data()
    
    # conexão a base de dados
    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vasco123',
    database=DB_NAME
    )
    cursor_def = conn.cursor()
    # list_data = [object_detect, date_detect]

    try:

        if len(database) == 0:
            sql = f'INSERT INTO {TABLE_NAME} (object_detect, date_detect) VALUES ("{object_detect}", "{date_detect}")'
        
            cursor_def.execute(sql)
            conn.commit()

        else:
            sql = f'INSERT INTO {TABLE_NAME} (object_detect, date_detect) VALUES ("{object_detect}", "{date_detect}")'
            
            cursor_def.execute(sql)
            conn.commit()
    except mysql.connector.errors.IntegrityError:
        pass

    cursor_def.close()
    conn.close()

def get_data():

    # conexão a base de dados
    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vasco123',
    database=DB_NAME
    )
    cursor_def = conn.cursor()

    cursor_def.execute(f'SELECT * FROM {TABLE_NAME}')
    database = cursor_def.fetchall()

    table_data = []

    for i in range(len(database)):
        _object, date = database[i]
        table_data.append([_object, date])

    cursor_def.close()
    conn.close()

    return table_data


def save_in_database(object_detect):
    date_detect = str(datetime.now())[:16]
    database = get_data()
    

    check_list = [object_detect, date_detect]
    if len(database) == 0:
        save_data_sql(check_list)
    else:

        if not check_list in database:
            save_data_sql(check_list)



cursor.close()
connection.close()


if __name__ == "__main__":

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='vasco123',
        database=DB_NAME
        )
    cursor = connection.cursor()

    sql = f'SELECT * FROM {TABLE_NAME}'

    cursor.execute(sql)
    database = get_data()

    # for a in range(len(database)):
    #     _id, _object, date = database[a]
    #     print(_id, _object, date)
    list_data = ['botle', '2024-09-05 03:15']

    if not list_data in database:
        print("não tem")

    else:
        print("tem")