

from ipwhois import IPWhois
from pprint import pprint
import json
import csv

filename = 'filteredip.txt'
lst = []
data =[]
with open(filename) as f:
    ip_list = f.readlines()
    ip_list = [x.rstrip('\n') for x in ip_list]
    print len(ip_list)

for ip in ip_list:
    obj = IPWhois(ip)
    results = obj.lookup_whois(inc_nir=True)
    for net_dict in (results.get('nets')):
        del net_dict['address']
        net_dict['ip'] = ip
        data.append(json.dumps(net_dict))
print data
'''with open("output"+ip+".csv","wb+") as f:  # python 2: open("output.csv","wb")
    title = "city,updated,handle,description,created,country,range,state,postal_code,ip,cidr,emails,name".split(",") # quick hack
    cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cw.writeheader()
    cw.writerows(data)
'''
