import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Соединение с postgres
connection = psycopg2.connect(user="postgres", password="qwerty123")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создание БД
cursor = connection.cursor()
cursor.execute('create database questions')

# Закрываем соединение
cursor.close()
connection.close()
