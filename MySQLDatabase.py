import MySQLdb

"""Как использовать:

Импортируйте класс:
from mysql_database import MySQLDatabase

Создайте объект класса:
db = MySQLDatabase(host="localhost", user="your_username", password="your_password")
# Укажите имя базы данных, если она уже существует:
db.connect()
# db.select_db("your_database_name") 

Выполните SQL-запросы:
results = db.select_query("SELECT * FROM your_table")
print(results)
db.insert_query("INSERT INTO your_table (column1, column2) VALUES ('value1', 'value2')")
db.update_query("UPDATE your_table SET column1='new_value' WHERE id=1")
db.delete_query("DELETE FROM your_table WHERE id=1")

Закройте соединение:
db.close_connection() 
Важно:
Установите библиотеку MySQLdb: pip install mysqlclient
"""

class MySQLDatabase:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.database
            )

            self.cursor = self.connection.cursor()
            # print("Соединение с базой данных установлено.")
        except MySQLdb.Error as err:
            print(f"Ошибка подключения к базе данных: {err}")

    def select_db(self, db_name):
        if self.connection:
            try:
                self.cursor.execute(f"USE {db_name}")
                self.database = db_name
                # print(f"База данных '{db_name}' выбрана.")
            except MySQLdb.Error as err:
                print(f"Ошибка выбора базы данных: {err}")

    def select_query(self, sql):
        if self.connection:
            try:
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                return results
            except MySQLdb.Error as err:
                print(f"Ошибка выполнения запроса: {err}")
                return None

    def insert_query(self, sql, value_to_insert):
        if self.connection:
            try:
                # self.cursor.execute(sql)
                self.cursor.execute(sql, value_to_insert)
                self.connection.commit()
                # print("Записи добавлены.")
            except MySQLdb.Error as err:
                print(f"Ошибка добавления записей: {err}")
                self.connection.rollback()

    def update_query(self, sql):
        if self.connection:
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                # print("Записи отредактированы.")
            except MySQLdb.Error as err:
                print(f"Ошибка редактирования записей: {err}")
                self.connection.rollback()

    def delete_query(self, sql):
        if self.connection:
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                # print("Записи удалены.")
            except MySQLdb.Error as err:
                print(f"Ошибка удаления записей: {err}")
                self.connection.rollback()

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            # print("Соединение с базой данных закрыто.")
