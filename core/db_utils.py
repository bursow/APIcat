

import sqlite3
from datetime import datetime


"""
Standart Database ismi aşağıdaki fonksiyonda yer almaktadır. Kaydedilecek veritabanın isimi buradan değiştirilebilir.

"""

def init_db(db_name="api_responses.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (url TEXT, method TEXT, status_code INTEGER, response TEXT, timestamp DATETIME)''')
    conn.commit()
    return conn


def save_response_to_db(conn, url, method, status_code, response_text):
    timestamp = datetime.now()
    c = conn.cursor()
    c.execute('INSERT INTO responses (url, method, status_code, response, timestamp) VALUES (?, ?, ?, ?, ?)',
              (url, method, status_code, response_text, timestamp))
    conn.commit()
