import os
import psycopg2


def conn():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='bibaboba', host='localhost',
                            port='5432')
    return conn