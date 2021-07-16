import sqlite3


# def jobskorea_create():
#     conn.execute(
#         'CREATE TABLE IF NOT EXISTS jobkorea1(id INTEGER, company TEXt, spec TEXT, loc TEXT, content TEXT, link TEXT);')


# jobskorea_create()


def jobskorea_insert(jobs):
    conn = sqlite3.connect("cbc.db")
    cur = conn.cursor()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS jobkorea(id INTEGER, company TEXT, spec TEXT, loc TEXT, content TEXT, link TEXT);')

    # print(jobs)
    for job in jobs:
        print(job)
        # cur.executemany('INSERT INTO jobkorea\
        # VALUES(?,?,?,?,?,?)', [(1001, "한박컴퍼니", "경력2년", "서울 강남구", "파이썬 개발",
        #                         "https://www.jobkorea.co.kr/Recruit/GI_Read/35291739?Oem_Code=C1&logpath=1"),
        #                        (49, '㈜무지개반사', '신입·경력2년↑', '서울 강남구', '[Python] 활용 딥러닝 개발자 모집',
        #                         'https://www.jobkorea.co.kr/Recruit/GI_Read/35301609?Oem_Code=C1&logpath=1')])

        cur.execute('INSERT INTO jobkorea\
        VALUES(?, ?, ?, ?, ?, ?)', (job["num"], job["company"], job["spec"], job["location"], job["content"], job["link"]))
        conn.commit()
    conn.close()
    return cur.lastrowid
