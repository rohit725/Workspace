from pymemcache.client.base import Client
import pandas as pd
import numpy as np
import unicodedata
import itertools
import logging
import sqlite3
import geoip2
import geoip2.database
import json
import time
import re


MP_files = ['Files/MP_C2s_data.txt', 'Files/MP_dgas_data.txt',
            'Files/MP_IPs_data.txt', 'Files/MP_sanit_URLs_data.txt']  # MP files path.
ransomware_files = ['Files/ransomwaretrackerdns.txt',
                    'Files/ransomwaretrackerip.txt', 'Files/ransomwaretrackerurl.txt']  # ransomware files path.
db_file = 'Files/datadump.db'  # put your database path for dumping the data into db.
directory = 'Files/'  # geodata dbs file directory path.


class ThreatIntel(object):
    def __init__(self):
        logging.basicConfig(filename="Files/dump_to_json.log",
                            format='%(asctime)s %(message)s', filemode='w')  # change file path for logger here.
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def read_txt(self, filename):
        try:
            df = pd.read_csv(filename, header=None)
        except Exception as e:
            self.logger.exception('read_txt: ' + str(e))
        return df

    def extract_ip(self, filename):
        # This method filters out ip from MP_C2s ip_domain column.
        try:
            df = filename['ip_domain_url'].str.extract(
                '(\d{1,3}\\.\d{1,3}\\.\d{1,3}\\.\d{1,3})', expand=True)
            df = df.fillna('')
            for count, value in enumerate(df[0]):
                if value != '':
                    filename.loc[count, 'ip_domain_url'] = value
        except Exception as e:
            self.logger.exception('extract_ip: ' + str(e))

    def rename_columns(self, dataframes):
        # Renaming columns of all the dataframes(just the needed once).
        try:
            dataframes[0] = dataframes[0].rename(
                columns={0: 'ip_domain_url', 1: 'malware', 2: 'timestamp'})
            dataframes[1] = dataframes[1].rename(
                columns={0: 'ip_domain_url', 1: 'dga', 2: 'timestamp'})
            dataframes[2] = dataframes[2].rename(
                columns={1: 'ip_domain_url', 3: 'malware', 4: 'timestamp'})
            dataframes[3] = dataframes[3].rename(columns={
                                                 0: 'timestamp', 1: 'ip_domain_url', 2: 'md5', 3: 'sha', 4: 'malware', 5: 'url', 6: 'filetype'})
            self.logger.info('Columns are renamed as needed...')
        except Exception as e:
            self.logger.exception('rename_columns: ' + str(e))
        return dataframes

    def time_format(self, series):
        # Converts integer timestamp to object type.
        try:
            def fun(x): return format(x, '.0f')
            series = series.apply(fun)
            self.logger.info('Timestamp is converted to object type...')
        except Exception as e:
            self.logger.exception('time format: ' + str(e))
        return series

    def ransomware_files(self, files):
        # Merges all file together from ransomware tracker.
        merged_df = None
        try:
            columns = ['ip_domain_url', 'domain', 'desc']
            dns_df = pd.read_csv(files[0], names=columns, comment='#')
            dns_df['domain_blocklist'] = np.nan
            ip_df = pd.read_csv(files[1], names=columns, comment='#')
            ip_df['rw_ip_blocklist'] = np.nan
            url_df = pd.read_csv(files[2], names=columns, comment='#')
            url_df['rw_url_blocklist'] = np.nan
            dns_df.domain_blocklist = dns_df.domain_blocklist.fillna(
                'RW_DOMBL')
            ip_df.rw_ip_blocklist = ip_df.rw_ip_blocklist.fillna('RW_IP')
            url_df.rw_url_blocklist = url_df.rw_url_blocklist.fillna(
                'RW_URL')
            merged_df = pd.concat([dns_df, ip_df, url_df], sort=False)
            merged_df.domain = merged_df.domain.fillna('abuse.ch')
            merged_df.desc = merged_df.desc.fillna('ransomware')
        except Exception as e:
            self.logger.exception(str(e))
        return merged_df

    def dumpsql(self, dictionary, db_file):
        # Dumps the dictionary into sqlite database.
        try:
            self.logger.info("Dumping the dictionary to database...")
            start_time = time.time()
            conn = sqlite3.connect(db_file)
            conn.execute("DROP TABLE IF EXISTS THREAT")
            conn.execute(
                "CREATE TABLE THREAT(IPURL TEXT NOT NULL, DATA TEXT NOT NULL)")
            for index in dictionary:
                data = str(dictionary[index])
                conn.execute(
                    "INSERT INTO THREAT(IPURL, DATA) VALUES(?, ?)", (index, data))
            conn.commit()
            conn.close()
            self.logger.info("The sql method takes %s second" %
                             (time.time() - start_time))
        except Exception as e:
            self.logger.exception('dumpsql: ' + str(e))

    def geoData(self, feedsPath, ip):
        # Returns a dictionary having physical location of given IP.
        try:
            geo_data = {'geo_info_mmdb': {}}
            reader = geoip2.database.Reader(feedsPath + '/GeoLite2-City.mmdb')
            reader2 = geoip2.database.Reader(feedsPath + '/GeoLite2-ASN.mmdb')
            response = reader.city(ip)
            response2 = reader2.asn(ip)
            if response:
                if response.continent.names.get('en', ''):
                    continent = (response.continent.names['en'])
                    continent = unicodedata.normalize(
                        'NFKD', continent).encode('ascii', 'ignore')
                else:
                    continent = ''
                if response.registered_country.names.get('en', ''):
                    country_reg = (response.registered_country.names['en'])
                    country_reg = unicodedata.normalize(
                        'NFKD', country_reg).encode('ascii', 'ignore')
                else:
                    country_reg = ''
                if response.country.names.get('en', ''):
                    country_name = (response.country.names['en'])
                    country_name = unicodedata.normalize(
                        'NFKD', country_name).encode('ascii', 'ignore')
                else:
                    country_name = ''
                if response.subdivisions.most_specific.name:
                    area = (response.subdivisions.most_specific.name)
                    area = unicodedata.normalize(
                        'NFKD', area).encode('ascii', 'ignore')
                else:
                    area = ''
                if response.city.name:
                    city_name = (response.city.name)
                    city_name = unicodedata.normalize(
                        'NFKD', city_name).encode('ascii', 'ignore')
                else:
                    city_name = ''
                if response.location.longitude:
                    longitude = str(response.location.longitude)
                else:
                    longitude = ''
                if response.location.latitude:
                    latitude = str(response.location.latitude)
                else:
                    latitude = ''
                if response.location.time_zone:
                    time_zone = (response.location.time_zone)
                    time_zone = unicodedata.normalize(
                        'NFKD', time_zone).encode('ascii', 'ignore')
                else:
                    time_zone = ''
                if response.postal.code:
                    postal_code = (response.postal.code)
                    postal_code = unicodedata.normalize(
                        'NFKD', postal_code).encode('ascii', 'ignore')
                else:
                    postal_code = ''
                geo_location = {'continent': continent, 'country_reg': country_reg, 'country_name': country_name, 'area': area,
                                'city_name': city_name, 'longitude': longitude, 'latitude': latitude, 'time_zone': time_zone, 'postal_code': postal_code}
            if response2:
                if response2.autonomous_system_organization:
                    aso = (response2.autonomous_system_organization)
                    aso = unicodedata.normalize(
                        'NFKD', aso).encode('ascii', 'ignore')
                else:
                    aso = ''
                if response2.autonomous_system_number:
                    asn = str(response2.autonomous_system_number)
                else:
                    asn = ''
                geo_location.update({'aso': aso, 'asn': asn})
                geo_data['geo_info_mmdb'] = geo_location
        except Exception as e:
            self.logger.exception('geoData: ' + str(e))
        return geo_data

    def dumpjson(self, dictionary):
        # Dumps a dictionary into file.
        try:
            self.logger.info('Writing dictionary into a file...')
            with open('Files/jsondata.txt', 'w') as f:
                json.dump(dictionary, f, indent=4)
        except Exception as e:
            self.logger.exception('dumpjson: ' + str(e))

    def fetchdata(self, start, end):
        # Select rows from the table between start and end given by user.
        try:
            conn = sqlite3.connect('Files/datadump.db')
            values = conn.execute(
                "SELECT * FROM THREAT WHERE ROWID BETWEEN {} AND {}".format(start, end))
            for row in values:
                print("{}\t{}".format(row[0], row[1]))
            conn.close()
        except Exception as e:
            self.logger.exception('fetchdata: ' + str(e))

    def remove_nans(self, dictionary):
        # Remove keys from the dictionary having nan values
        try:
            lst = []
            for dct in dictionary:
                data = {key: dct[key] for key in dct if pd.notna(dct[key])}
                lst.append(data)
            self.logger.info('Nans removed...')
        except Exception as e:
            self.logger.exception('remove_nans: ' + str(e))
        return lst

    def group_dict(self, dictionary):
        # grouping the dictionary according to ip_domain_url column
        try:
            grouped_dct = {}
            for key, group in itertools.groupby(dictionary, key=lambda x: x['ip_domain_url']):
                new_dct = {}
                new_lst = []
                for dct in list(group):
                    dct.pop('ip_domain_url')
                    new_lst.append(dct)
                new_dct['data'] = new_lst
                grouped_dct[key] = new_dct
            self.logger.info(
                'Dictionary grouped according to IP/Domain/Urls...')
        except Exception as e:
            self.logger.exception('group_dict: ' + str(e))
        return grouped_dct

    def add_geodata(self, dictionary):
        # Method to add key geo_info_mmdb to each key in dictionary.
        try:
            for index in dictionary:
                if re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', index):
                    dictionary[index].update(self.geoData(directory, index))
                else:
                    geo_data = {'geo_info_mmdb': {}}
                    dictionary[index].update(geo_data)
        except Exception as e:
            self.logger.exception('add_geodata: ' + str(e))
        return dictionary

    def dumpmemcache(self, dct):
        # Method to dump dictionary to memcache.
        try:
            client = Client(
                ('localhost', 11211), serializer=self.json_serializer, deserializer=self.json_deserializer)
            self.logger.info("Dumping dictionary to memcache...")
            for key, value in dct.iteritems():
                # memcache only supports 250 character long keys without whitespaces.
                if len(key) > 250:
                    key = key[:250]
                client.set(key, value, expire=100)
        except Exception as e:
            self.logger.exception('dumpmemcache: ' + str(e))

    def json_serializer(self, key, value):
        # Serializer for the client in dumpmemcache method.
        if type(value) == str:
            return value, 1
        return json.dumps(value), 2

    def json_deserializer(self, key, value, flags):
        # Deserializer for the client in dumpmemcache method.
        try:
            if flags == 1:
                return value
            if flags == 2:
                return json.loads(value)
            raise Exception("Unknown serialization format")
        except Exception as e:
            self.logger.exception(str(e))

    def filter_dictionary(self, dictionary):
        try:
            self.logger.info('Starting filter...')
            for index in dictionary:
                data = dictionary[index]['data']
                count = 0
                length = len(data)
                dga_list = []
                sanit_list = []
                ransomware = {}
                malware_list = []
                while count < length:
                    domainb = data[count]['domain_blocklist']
                    ipb = data[count]['rw_ip_blocklist']
                    urlb = data[count]['rw_url_blocklist']
                    domain = data[count]['domain']
                    desc = data[count]['desc']
                    dga = data[count]['dga']
                    time = data[count]['timestamp']
                    md5 = data[count]['md5']
                    sha = data[count]['sha']
                    malware = data[count]['malware']
                    url = data[count]['url']
                    filetype = data[count]['filetype']
                    if domain != '' and desc != '':
                        if domainb != '':
                            ransomware['domain_blocklist'] = domainb
                        if ipb != '':
                            ransomware['rw_ip_blocklist'] = ipb
                        if urlb != '':
                            ransomware['rw_url_blocklist'] = urlb
                        ransomware['domain'] = domain
                        ransomware['desc'] = desc
                        del data[count]
                        length = length - 1
                    elif dga != '':
                        temp_dict = {'timestamp': time, 'dga': dga}
                        dga_list.append(temp_dict)
                        del data[count]
                        length = length -1
                    elif md5 != '' or sha != '':
                        temp_dict = {'malware': malware, 'timestamp': time, 'md5': md5, 'sha': sha, 'url': url, 'filetype': filetype}
                        sanit_list.append(temp_dict)
                        del data[count]
                        length = length -1
                    elif md5 == '' and sha == '' and malware != '':
                        temp_dict = {'malware': malware, 'timestamp': time}
                        malware_list.append(temp_dict)
                        del data[count]
                        length = length - 1
                    else:
                        count = count + 1
                dictionary[index]['ransomwaretracker'] = ransomware
                dictionary[index]['dga'] = dga_list
                dictionary[index]['saniturl'] = sanit_list
                dictionary[index]['malware'] = malware_list
                if data:
                    dictionary[index]['data'] = data
                else:
                    dictionary[index].pop('data')
        except Exception as e:
            self.logger.exception('add_ransomware: ' + str(e))
        return dictionary


def main():
    try:
        start_time = time.time()
        # Loading the files.
        threatIntelObj = ThreatIntel()
        dataframes = []
        for filename in MP_files:
            dataframes.append(threatIntelObj.read_txt(filename))
        threatIntelObj.logger.info('Files are loaded in dataframe...')

        # Renaming columns, timestamp formating and extracting ip.
        dataframes = threatIntelObj.rename_columns(dataframes)
        dataframes[2]['timestamp'] = threatIntelObj.time_format(
            dataframes[2]['timestamp'])
        threatIntelObj.extract_ip(dataframes[0])
        threatIntelObj.logger.info('Dataframes are filtered as needed...')

        # Dropping unnecessary columns from dataframes.
        df = dataframes[2]
        dataframes[2] = df.drop(df.columns[[0, 2]], axis=1)
        threatIntelObj.logger.info('Unnecessary column dropped...')

        # Concatinating all the dataframes in one dataframe.
        ransomware_df = threatIntelObj.ransomware_files(ransomware_files)
        dataframes.append(ransomware_df)
        merged_df = pd.concat(dataframes, sort=False)
        threatIntelObj.logger.info('All dataframes merged into one...')

        # Sorting and removing duplicates from the dataframe.
        sorted_df = merged_df.sort_values(by=['ip_domain_url'])
        dupl_removed_df = pd.DataFrame.drop_duplicates(sorted_df)
        final_df = dupl_removed_df.fillna('')
        threatIntelObj.logger.info('Duplicate rows removed...')

        # Converting Dataframe to Dictionary.
        dct = final_df.to_dict('records')
        threatIntelObj.logger.info('Dataframes converted to dictionary...')

        # Removing Nan, group according to ip and add geodata.
        #dct = threatIntelObj.remove_nans(dct)
        grouped_dct = threatIntelObj.group_dict(dct)
        grouped_dct = threatIntelObj.filter_dictionary(grouped_dct)
        grouped_dct = threatIntelObj.add_geodata(grouped_dct)

        # Dumping.
        # threatIntelObj.dumpjson(grouped_dct)
        threatIntelObj.dumpsql(grouped_dct, db_file)
        # threatIntelObj.fetchdata(10000, 10050)
        # threatIntelObj.dumpmemcache(grouped_dct)
        print('Done! It took %s seconds to run.' % (time.time() - start_time))
    except Exception as e:
        threatIntelObj.logger.exception('main: ' + str(e))


if __name__ == '__main__':
    main()
