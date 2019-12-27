#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  get_data_misp.py
#  
#  Copyright 2019 Unknown <rpandey@dev-master>
#  
#  
import traceback
import os


def main(args):
    try:
        ips = None
        with open("Files/ips.txt") as fp:
            ips = fp.readlines()
        ips = [x.strip("\r\n") for x in ips]
        for ip in ips:
            cmd = "/opt/virtenv/pymaster3/bin/python3 Misp_search.py -p values -a -s %s -o %s.json" % (ip, ip.replace(".", "_"))
            os.system(cmd)
    except Exception as err:
        print(str(err))
        print(traceback.format_exc())
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
