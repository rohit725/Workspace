import pandas as pd
import time
import re
import os


load_file = 'Files/normal_tweets.csv'
save_file = 'Files/filtered_normal_tweets.csv'


class Filterti(object):
    def __init__(self):
        if os.path.isfile(load_file):
            self.norm_df = pd.read_csv(load_file, encoding='utf-8')
        else:
            self.norm_df = None

    def ip_domain_url_filter(self, text):
        ip_list = re.findall(
            r"\d{1,3}(?:\[|\()?\.(?:\]|\))?\d{1,3}(?:\[|\()?\.(?:\]|\))?\d{1,3}(?:\[|\()?\.(?:\]|\))?\d{1,3}", str(text))
        if '1.3.0.4' in ip_list:
            ip_list.remove('1.3.0.4')
        raw_url_list = re.findall(
            r"(?:(?:http?|hxxp?|hxxps?|https):\/\/)[\w/\-?=%.\[\(\]\)]+\.[\w/\-?=%.\]\)\[\(]+", str(text))
        url_list = []
        if raw_url_list:
            for url in raw_url_list:
                if not (url.startswith('https://t.co') or url.startswith('https://twitter.com') or url.startswith('hxxps://twitter.com')):
                    url_list.append(url)
        if url_list:
            domain_list = [
                re.search(r"[\w\-?=%.\[\(]+\.[\w\-?=%.\)\]]+", str(url)) for url in url_list]
            domain_list = [x.group(0) for x in domain_list if x is not None]
        else:
            domain_list = []
        ip_list.extend(url_list)
        ip_list.extend(domain_list)
        for count, ip in enumerate(ip_list):
            if '[' in ip:
                # print("found")
                ip_list[count] = ip.replace('[', '')
            if '(' in ip:
                ip_list[count] = ip.replace('(', '')
            if ']' in ip:
                ip_list[count] = ip.replace(']', '')
            if ')' in ip:
                ip_list[count] = ip.replace(')', '')
        ip_list = list(set(ip_list))
        if ip_list:
            return ip_list
        else:
            return ''

    def md5_filter(self, text):
        md5_list = re.findall(r"[0-9a-f\$]{32}", str(text))
        if md5_list:
            return md5_list
        else:
            return ''

    def filter(self):
        start = time.time()
        if self.norm_df is not None:
            df = None
            if os.path.isfile(save_file):
                df = pd.read_csv(save_file, encoding='utf-8')
            self.norm_df['ip_domain_urls'] = self.norm_df.tweet.map(
                lambda s: self.ip_domain_url_filter(s))
            self.norm_df['md5'] = self.norm_df.tweet.map(
                lambda s: self.md5_filter(s))
            self.norm_df = self.norm_df[self.norm_df['ip_domain_urls'] != '']
            self.norm_df = self.norm_df.drop('tweet', axis=1)
            if df is not None:
                self.norm_df = pd.concat([df, self.norm_df], sort=True)
            self.norm_df = self.norm_df.astype(str).drop_duplicates('ip_domain_urls')
            self.norm_df.to_csv(save_file, index=False)
            cmd = "rm -f " + load_file
            os.system(cmd)
            print('Normal tweets filter took %s seconds' %
                  (time.time() - start))
        else:
            print("No such file to load tweets from.")


if __name__ == '__main__':
    filtertObj = Filterti()
    filtertObj.filter()
