import mysql.connector

def get_db_connection():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='docker',
        database='sicoob'
    )

    return conexao