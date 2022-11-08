import psycopg2

import os

DB_URL = os.environ.get('DATABASE_URL', 'dbname=meal_planner')

conn = psycopg2.connect(DB_URL)


def sql_select_all(query, params=[]):
    cur = conn.cursor()
    cur.execute(query, params)

    return cur
    

def sql_select_one(query, params=[]):
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    cur.close()

    return result


def sql_write(query, params=[]):
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
