from __future__ import print_function

import datetime
import warnings

import MySQLdb as mdb
import requests

db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'polad2003'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]