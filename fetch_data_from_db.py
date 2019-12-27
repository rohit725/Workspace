import sqlite3
from xlwt import Workbook


def main():
    ip_list = []
    conn = sqlite3.connect("Files/threat_intel.db")
    wb = Workbook()
    count = 1
    sheet1 = wb.add_sheet('sheet 1')
    sheet1.write(0, 0, 'ip')
    sheet1.write(0, 1, 'tag')
    with open('Files/ips.txt', 'r') as f:
        txt = f.read()
        ip_list = txt.strip().split('\n')
        ip_list = [i for i in ip_list if i]
        print(len(ip_list))
    for ip in ip_list:
        query = "select * from tidata where ip_domain_url='%s'" % (ip)
        value = conn.execute(query).fetchone()
        if value:
            data = eval(value[1])
            if data['malware']:
                sheet1.write(count, 0, ip)
                sheet1.write(count, 1, data['malware'][0]['malware'])
                count += 1
            else:
                print('Not a malware')
        else:
            print("No data from db.")
    wb.save('Files/ip_data.xls')


if __name__ == '__main__':
    main()
