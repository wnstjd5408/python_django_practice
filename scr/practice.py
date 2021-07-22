import sqlite3


conn = sqlite3.connect("employee.db")
cur = conn.cursor()
conn.execute(
    'CREATE TABLE employee_data(id INTEGER, name TEXT, nickname TEXT, department TEXT, employment_date TEXT)')
cur.executemany('INSERT INTO employee_data VALUES (?, ?, ?, ?, ?)', [(1001, 'Donghyun', 'SOMJANG', 'Development', '2020-04-01 00:00:00.000'), (2001, 'Sol', 'Fairy', 'Marketing', '2020-04-01 00:00:00.000'), (
    2002, 'Jiyoung', 'Magician', 'Marketing', '2020-04-01 00:00:00.000'), (1002, 'Hyeona', 'Theif', 'Development', '2020-04-01 00:00:00.000'), (1003, 'Soyoung', 'Chief', 'Development', '2020-04-01 00:00:00.000')])
conn.commit()
conn.close()
