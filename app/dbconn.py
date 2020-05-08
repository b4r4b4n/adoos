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
    conn = psycopg2.connect(dbname='d2kdscukj077tc', user='cgpgjldttlacbu',
    password='12285c7849e06b03953c225161a11fa2e13347185714bf3e83a7e123940f1fd7',
    host='ec2-34-200-116-132.compute-1.amazonaws.com',
    port='5432')
    return conn