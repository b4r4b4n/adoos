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
    conn = psycopg2.connect(dbname='d5ft4rhm6bmstn', user='wewmgokdtzuamc',
    password='583ad885255b9e54e4b65c2cd410954faab0a0f146349d57787caddcfe29da50',
    host='ec2-3-222-150-253.compute-1.amazonaws.com',
    port='5432')
    return conn