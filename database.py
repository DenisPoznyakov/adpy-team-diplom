import sqlalchemy
from sqlalchemy.orm import sessionmaker

driver_db = input('Введите название СУБД: ')
login = input('Введите имя пользователя: ')
password = input('Введите пароль: ')
host = input('Введите host сервера: ')
port = input('Введите порт сервера: ')
name_db = input('Введите название БД: ')


DSN = f'{driver_db}://{login}:{password}@{host}:{port}/{name_db}

engine = sqlalchemy.create_engine(DSN)

session = sessionmaker(bind=engine)
