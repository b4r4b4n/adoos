import os
import urllib.parse as urlparse
import psycopg2

#url = urlparse.urlparse(os.environ['DATABASE_URL'])
#dbname = url.path[1:]
#user = url.username
#password = url.password
#host = url.hostname
#port = url.port


def conn():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
    password='bibaboba',
    host='localhost',
    port='5432')
    return conn