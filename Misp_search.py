#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Misp_search.py
#  
#  Copyright 2019 Unknown <rpandey@dev-master>
#  
#  


from pymisp import PyMISP
import traceback
import argparse
import json
import os



# you can take this arguments from conf file or use it directly.
MISP_URL = "https://165.22.32.210/"
MISP_API_KEY = "B47xVb1dcAxt9uOqWHAyzMoBnvCYhyYbmzzeafps"


class Misp:
    def __init__(self, url, key):
        self.misp = PyMISP(url, key, False, 'json')

    def search(self, quiet, url, controller, out=None, **kwargs):
        try:
            result = self.misp.search(controller, **kwargs)
            if quiet:
                for e in result['response']:
                    print('{}{}{}\n'.format(url, '/events/view/', e['Event']['id']))
            elif out is None:
                print(json.dumps(result['response']))
            else:
                with open(out, 'w') as f:
                    f.write(json.dumps(result['response']))
        except Exception as err:
            print(err)
            print(traceback.format_exc())


# For testing purpose used argparser to take argument from commandline change it as you need.
def main():
    parser = argparse.ArgumentParser(description='Get all the events matching a value for a given param.')
    parser.add_argument("-p", "--param", required=True, help="Parameter to search (e.g. category, org, values, type_attribute, etc.)")
    parser.add_argument("-s", "--search", required=True, help="String to search.")
    parser.add_argument("-a", "--attributes", action='store_true', help="Search attributes instead of events")
    parser.add_argument("-q", "--quiet", action='store_true', help="Only display URLs to MISP")
    parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if args.output is not None and os.path.exists(args.output):
        print('Output file already exists, abort.')
        exit(0)

    # Creating an object of Misp class
    misp_obj = Misp(MISP_URL, MISP_API_KEY)
    kwargs = {args.param: args.search}

    if args.attributes:
        controller='attributes'
    else:
        controller='events'

    # Invoking the method which will search for the attributes or events in MISP. 
    misp_obj.search(args.quiet, MISP_URL, controller, args.output, **kwargs)


if __name__ == '__main__':
    main()
