from fastapi import HTTPException, status
import psycopg2
from psycopg2 import errors
# from psycopg2 import pool
# from contextlib import contextmanager
#
# from core import settings
#
# # from app.core.config import settings
#
# db_pool = pool.SimpleConnectionPool(
#     1, 10,
#     host=settings.DB_HOST,
#     database=settings.DB_NAME,
#     user=settings.DB_USER,
#     password=settings.DB_PASSWORD,
#     port=settings.DB_PORT,
# )
#
# @contextmanager
# def get_conn():
#     conn = db_pool.getconn()
#     try:
#         yield conn
#     finally:
#         db_pool.putconn(conn)


import psycopg2

from core import settings


class DataBase:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=settings.DB_HOST,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                port=settings.DB_PORT
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao conectar como banco de dados! Verifique se as informações estão corretas'
            )
        

    def _get_conn(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="your_database",
            user="your_user",
            password="your_password",
            port="5432"
        )


    def execute(self, sql, params=None, many=True):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall() if many else cursor.fetchone()
            cursor.close()
            self.conn.close()
            return result
    
        except errors.UndefinedTable as e:
            cursor.close()
            self.conn.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='A tabela não existe no banco de dados!'
            )
        
        except Exception as e:
            cursor.close()
            self.conn.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Erro ao executar consulta!'
            )


    def commit(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return result
        except errors.UndefinedTable as e:
            cursor.close()
            self.conn.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='A tabela não existe no banco de dados!'
            )
