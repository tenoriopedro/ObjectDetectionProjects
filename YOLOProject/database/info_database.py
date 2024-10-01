#### Modulo para buscar informações do banco de dados

import mysql.connector

DB_NAME = "database_detect"
TABLE_NAME = "info_object"

connection = mysql.connector.connect(
    host="localhost",
    user='root',
    password='vasco123',
    database=DB_NAME
)

cursor = connection.cursor()

cursor.execute(
    f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} "
    "("
    "id INTEGER NOT NULL AUTO_INCREMENT, "
    "object_detect VARCHAR(100) NOT NULL, "
    "description_object VARCHAR(1000) NOT NULL, "
    "link_object VARCHAR(1000) NOT NULL, "
    "image_path VARCHAR(1000) NOT NULL, "
    "PRIMARY KEY (id)"
    ")"
)

def insert_into_database():

    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='vasco123',
        database=DB_NAME
    )
    cursor_def = conn.cursor()

    object_detect = "telemovel"
    description_object = "Este telemovel tem cor preta"
    link_object = "https://pt.wikipedia.org/wiki/Telefone_celular"
    image_path = "C:/Desenvolvimento/ProjetoYOLOWebcam02/image/telemovel.png"

    sql = f'INSERT INTO {TABLE_NAME} (object_detect, description_object, link_object, image_path) VALUES ("{object_detect}", "{description_object}", "{link_object}", "{image_path}")'

    cursor_def.execute(sql)
    conn.commit()


    cursor_def.close()
    conn.close()


def get_info():
    
    conn = mysql.connector.connect(
        host="localhost",
        user='root',
        password='vasco123',
        database=DB_NAME
    )
    cursor_def = conn.cursor()

    sql = f'SELECT * FROM {TABLE_NAME}'
    cursor_def.execute(sql)
    data_info = cursor_def.fetchall()

    list_data = []

    _id, object_detect, description_object, link_object, image_path = data_info[0]
    _id01, object_detect01, description_object01, link_object01, image_path01 = data_info[1]
    _id02, object_detect02, description_object02, link_object02, image_path02 = data_info[2]

    list_data.append([object_detect, description_object, link_object, image_path])
    list_data.append([object_detect01, description_object01, link_object01, image_path01])
    list_data.append([object_detect02, description_object02, link_object02, image_path02])

    cursor_def.close()
    conn.close()
    return list_data


cursor.close()
connection.close()

if __name__ == "__main__":
    # insert_into_database()

    connection = mysql.connector.connect(
        host="localhost",
        user='root',
        password='vasco123',
        database=DB_NAME
        )

    cursor = connection.cursor()
    list = []
    sql = f'SELECT * FROM {TABLE_NAME}'
    cursor.execute(sql)
    data = cursor.fetchall()

    _id, object_detect, description_object, link_object, image_path = data[0]
    _id01, object_detect01, description_object01, link_object01, image_path01 = data[1]
    _id02, object_detect02, description_object02, link_object02, image_path02 = data[2]
    class_names = ["pessoa", "comando"]
    list.append([object_detect, description_object, link_object, image_path])
    list.append([object_detect01, description_object01, link_object01, image_path01])
    list.append([object_detect02, description_object02, link_object02, image_path02])
    count = 1
    for name in range(len(class_names)):
        for i in list:
            temporary_list = []
            if class_names[name] in i:
                object, description, link, image = i
                temporary_list.append((object, description, link))
                for data in temporary_list:
                    print(f"{count}-", end=" ")
                    for k, line in enumerate(data):

                        print(line)
                count += 1
    # for name in range(len(class_names)):
    #     for i in list:
    #         if class_names[name] in i:
    #             for k, line in enumerate(i):
    #                 print(line)



