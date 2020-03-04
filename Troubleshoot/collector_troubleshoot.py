#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  collector_troubleshoot.py
#  
#  Copyright 2019 Unknown <rpandey@dev-master>
#  
#  

from paramiko_expect import SSHClientInteraction
import elasticsearch
import traceback
import argparse
import getpass


class Troubleshoot:
    def __init__(self, eshost_ip):
        self.es = elasticsearch.Elasticsearch(eshost_ip + ":9200")


def main(args):
    try:
        parser = argparse.ArgumentParser(prog="Scanned Files Troubleshoot")
        parser.add_argument(
            "-ip", help="IP address of remote server(master)", type=str)
        parser.add_argument(
            "-u", "--user", help="User name of remote server", type=str, default="root")
        parser.add_argument("-p", "--password", help="Password of remote server",
                            type=str, default="1844di@lG14Solutions")
        parser.add_argument(
            "-l", "--lines", help="Number of lines to print in logs", default="10", type=str)
        parser.add_argument("-sid", help="sensor id", type=str)
        parser.add_argument("-esip", help="IP for elastic search connectio.", type=str)
        args = parser.parse_args()
        if not (args.ip and args.lines and args.sid):
            raise Exception("Please provide necessary parameters.")
        hostname = args.ip
        username = args.user
        password = args.password
        lines = args.lines
        sid = args.sid
    except Exception as err:
        print(err)
        print(traceback.format_exc())
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
