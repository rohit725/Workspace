import sqlite3
import os


def fetch_data():
    db_file = 'datadump.db'
    filename = 'input_ips.txt'
    lst = []
    with open(filename) as f:
        ip_list = f.readlines()
        ip_list = [x.rstrip('\n') for x in ip_list]
        print len(ip_list)
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        counter = 0
        for ip in ip_list:
            cur.execute(
               "SELECT * FROM THREAT WHERE IPURL='{}'".format(ip))
            value = cur.fetchall()
            if value:
                counter += 1
                print(ip)
                lst.append(ip)
            else:
                print('.')
        conn.close()
    except Exception as e:
        print 'fetchdata: ' + str(e)
    with open('filteredip.txt', 'w') as f:
        f.write('Count: %s \n'%(counter))
        for ip in lst:
            f.write(ip + '\n')


fetch_data()
