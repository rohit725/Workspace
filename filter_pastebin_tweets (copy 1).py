import pandas as pd
import traceback
import requests
import urllib
import time
import re
import os


load_file = 'Files/pastebin_tweets.csv'
save_file = 'Files/filtered_pastebin_tweets.csv'


class Filterti(object):
    def __init__(self):
        if os.path.isfile(load_file):
            self.paste_df = pd.read_csv(load_file, encoding='utf-8')
        else:
            self.paste_df = None

    def scrape_pastebin_urls(self, pastebin_urls):
        paste_keys = []
        ip_domain_urls = []
        for url in pastebin_urls:
            if url.startswith('https'):
                try:
                    response = requests.get(url, timeout=(4, 5))
                except Exception as e:
                    print('Request unsuccessful for %s' % (url))
                    print(e)
                    continue
                if response.status_code == 200:
                    try:
                        if response is not None and response.url.startswith('https://pastebin.com/'):
                            print('Its a pastebin url: %s' % (response))
                            ip_domain_urls.append(response.url)
                            #u = re.findall(r"([^\/?]+)(?:\?.+)?$", response.url)
                            #for items in u:
                                #paste_keys.append(items)
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                        continue
        #if paste_keys:
            #for key in paste_keys:
                #base = 'https://scrape.pastebin.com/api_scrape_item.php?i=' + key
                #page = urllib.request.urlopen(base).read().decode("utf-8")
                #time.sleep(1)
                #page = page.split("\r\n")
                #for data in page:
                    #ip_list = re.findall(
                        #r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", data)
                    #url_list = re.findall(
                        #r"(?:(?:hxxp?|http?|https?|hxxps):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+", data)
                    #domain_list = re.findall(
                        #r"^[\w\-?=%.]+\.[\w/\-?=%.]+$", data)
                #ip_domain_urls.extend(ip_list)
                #ip_domain_urls.extend(url_list)
                #ip_domain_urls.extend(domain_list)
        if ip_domain_urls:
            return ip_domain_urls
        else:
            return ''

    def filter(self):
        start = time.time()
        if self.paste_df is not None:
            print('length of df: %s' % (len(self.paste_df)))
            if os.path.isfile(save_file):
                dfObj = pd.read_csv(save_file, encoding='utf-8')
            else:
                dfObj = pd.DataFrame(columns=[
                    'created_at', 'ip_domain_urls', 'user_name', 'user_id', 'follower_count', 'hash_tag/user'])
            count = 0
            for index, row in self.paste_df.iterrows():
                shortlinks = list(eval(row['twitter_shortlinks']))
                if (count + len(shortlinks)) < 250:
                    ip_domain_urls = self.scrape_pastebin_urls(shortlinks)
                    ind = len(dfObj)
                    dfObj.loc[ind] = [row['created_at'], ip_domain_urls, row['user_name'],
                                      row['user_id'], row['follower_count'], row['hash_tag/user']]
                    self.paste_df.drop(index, inplace=True)
                    count += len(row)
                else:
                    break
            dfObj = dfObj[dfObj['ip_domain_urls'] != '']
            if not self.paste_df.empty:
                print('length of df: %s' % (len(self.paste_df)))
                self.paste_df.to_csv(load_file, index=False)
            dfObj.to_csv(save_file, index=False)
            print('Pastebin data filter took %s seconds' %
                  (time.time() - start))
        else:
            print("No such file to load tweets from.")


if __name__ == '__main__':
    filtertObj = Filterti()
    filtertObj.filter()
