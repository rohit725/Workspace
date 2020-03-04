from sqlalchemy import create_engine
from pymemcache.client import base
from os import path
import pandas as pd


db_file = "/opt/blusapphire/content/threat_intel.db"


def main():
    if path. isfile(db_file):
        conn = create_engine('sqlite:///%s' % db_file, echo=False)
        df = pd.read_sql_table("tidata", con=conn)
        #print(df.head(20))
        #print(df.tail(20))
        conn.dispose()
    client = base.Client(('localhost', 11211))
    df = df.apply(lambda x: x['ip_domain_url']=x[ip_domain_url][:200], axis=1)
    df.apply(lambda x: client.set(x['ip_domain_url'], x['value']), axis=1)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
