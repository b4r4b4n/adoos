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
                            password='bibaboba', host='localhost',
                            port='5432')
    #conn = psycopg2.connect(psycopg2.connect(
     #       dbname=dbname,
      #      user=user,
      #      password=password,
      #      host=host,
      #      port=port
      #      ))

       # (dbname='dfrgf19s062bbn', user='bvvpnjzzpsmnza',                         password='ff46da3c8bebe99e98fc38b8787396ad0b1daedf39bc0a0c8acf09d6ad408677', host='ec2-174-129-254-223.compute-1.amazonaws.com',                            port=process.env.PORT)
    return conn