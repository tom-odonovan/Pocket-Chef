import psycopg2

conn = psycopg2.connect('dbname=meal_planner')


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
