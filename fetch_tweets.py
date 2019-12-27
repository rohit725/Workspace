from multiprocessing import Pool
import pandas as pd
import datetime
import tweepy
import time
import re


_access_key = '1082853714631618560-ONpn8MT8LdD9xDWE67SxlmgnQIemwW'
_access_secret = 'i0K5s1mtuBvwJmVBUwZL3aLbi0r1n1G0WjINIqljxLKjr'
_consumer_key = 'Eptv6pbQqHrnNHiwlKaiIMNBa'
_consumer_secret = 'EE8xuCIeAmLZHP7kmnyWhOpEoiQP6dKiMkjVWCSbvz1Hbj5dK6'

_auth = tweepy.OAuthHandler(_consumer_key, _consumer_secret)
_auth.set_access_token(_access_key, _access_secret)

# File path to generate normal tweets csv.
normalcsv = 'Files/normal_tweets.csv'
# File path to generate pastebin tweets csv.
pastecsv = 'Files/pastebin_tweets.csv'


class TiData(object):
    """Fetches tweets from tweeter related to some
            specific tags or user."""

    def createDataframeFromTag(self, hash_name):
        try:
            print('Creating dataframe from tag: %s' % (hash_name))
            api = tweepy.API(_auth, wait_on_rate_limit=True)
            time_span_days = 30
            current_date = datetime.date.today()
            dfObj = pd.DataFrame(columns=[
                                 'created_at', 'tweet', 'user_name', 'user_id', 'follower_count', 'hash_tag/user'])
            c = tweepy.Cursor(api.search, q="%s" % hash_name, count=100,
                              lang="en", since=current_date - datetime.timedelta(days=time_span_days), until=current_date, tweet_mode='extended').items()
            while True:
                try:
                    tweet = c.next()
                    index = len(dfObj)
                    created_at = tweet.created_at
                    text = tweet.full_text
                    if text[0:3] == 'RT ':
                        try:
                            text = tweet.retweeted_status.full_text.encode(
                                'utf-8')
                        except AttributeError:
                            text = text.encode('utf-8')
                            pass
                    screen_name = tweet.user.screen_name
                    tid = tweet.user.id
                    followers = tweet.user.followers_count
                    # print(created_at, text, screen_name, tid, followers)
                    dfObj.loc[index] = [created_at, text,
                                        screen_name, tid, followers, hash_name]
                except tweepy.TweepError as e:
                    print('failed on_status,', str(e))
                    print("sleeping for 15 mins.")
                    time.sleep(60 * 15)
                    continue
                except StopIteration:
                    break
        except Exception as e:
            print('createDataframeFromTag: ' + str(e))
        return dfObj

    def createDataframeFromUser(self, screen_name):
        try:
            print('Creating dataframe from user: %s' % (screen_name))
            api = tweepy.API(_auth, wait_on_rate_limit=True)
            dfObj = pd.DataFrame(columns=[
                                 'created_at', 'tweet', 'user_name', 'user_id', 'follower_count', 'hash_tag/user'])
            all_tweets = []
            oldest = 0
            while True:
                try:
                    if oldest == 0:
                        new_tweets = api.user_timeline(
                            screen_name=screen_name, count=500, tweet_mode='extended')
                    else:
                        new_tweets = api.user_timeline(
                            screen_name=screen_name, count=500, max_id=oldest, tweet_mode='extended')
                    if new_tweets:
                        all_tweets.extend(new_tweets)
                        oldest = all_tweets[-1].id - 1
                    else:
                        break
                except tweepy.TweepError as e:
                    print('failed on_status,', str(e))
                    print("sleeping for 15 mins.")
                    time.sleep(60 * 15)
                    continue
                for tweet in all_tweets:
                    index = len(dfObj)
                    created_at = tweet.created_at
                    text = tweet.full_text
                    if text[0:3] == 'RT ':
                        try:
                            text = tweet.retweeted_status.full_text.encode(
                                'utf-8')
                        except AttributeError:
                            text = text.encode('utf-8')
                            pass
                    screen_name = tweet.user.screen_name
                    tid = tweet.user.id
                    followers = tweet.user.followers_count
                    # print(created_at, text, screen_name, tid, followers)
                    dfObj.loc[index] = [created_at, text,
                                        screen_name, tid, followers, screen_name]
        except Exception as e:
            print('createDataframeFromUser: ' + str(e))
        return dfObj

    def mergeAllDataframes(self):
        try:
            start = time.time()
            pool = Pool(processes=5)
            hash_tags = ['#malware', '#spam',
                         '#opendir', '#ransomware', '#Phishing']
            users = ['@PhishingAi', '@VK_Intel', '@shotgunner101', '@bad_packets']
            tags_list = [{'func': 'createDataframeFromTag', 'value': y}
                         for y in hash_tags]
            users_list = [{'func': 'createDataframeFromUser', 'value': y}
                          for y in users]
            normal_dfs = []
            for df in pool.map(self, tags_list):
                if not df.empty:
                    normal_dfs.append(df)
            for df in pool.map(self, users_list):
                if not df.empty:
                    normal_dfs.append(df)
            pastebin_users = ['@Mesiagh', '@Cryptolaemus1']
            pastebin_dfs = []
            for df in pool.map(self.createDataframeFromUser, pastebin_users):
                if not df.empty:
                    pastebin_dfs.append(df)
            merged_dfs = pd.concat(normal_dfs, sort=False)
            merged_dfs = merged_dfs.sort_values(by=['user_name'])
            merged_dfs = pd.DataFrame.drop_duplicates(merged_dfs)
            merged_pastebins = pd.concat(
                pastebin_dfs, sort=False)
            merged_pastebins = merged_pastebins.sort_values(by=['user_name'])
            merged_pastebins = pd.DataFrame.drop_duplicates(merged_pastebins)
            if not merged_dfs.empty:
                merged_dfs.to_csv(normalcsv, index=False)
            if not merged_pastebins.empty:
                merged_pastebins['twitter_shortlinks'] = merged_pastebins.tweet.map(
                    lambda s: self.twitter_shortlinks(s))
                merged_pastebins = merged_pastebins[merged_pastebins['twitter_shortlinks'] != '']
                merged_pastebins = merged_pastebins.drop('tweet', axis=1)
                with open(pastecsv, 'a') as f:
                    merged_pastebins.to_csv(
                        f, mode='a', index=False, header=f.tell() == 0)
            print("Total time taken: %s" % (time.time() - start))
        except Exception as e:
            print('mergeAllDataframes: ' + str(e))

    def __call__(self, x):
        try:
            if x["func"] == "createDataframeFromTag":
                return self.createDataframeFromTag(x["value"])
            if x["func"] == "createDataframeFromUser":
                return self.createDataframeFromUser(x["value"])
        except Exception as e:
            print('__call__: ' + str(e))

    def twitter_shortlinks(self, text):
        url_list = re.findall(
            r"https://[\w/\-?=%.]+\.[\w/\-?=%.]+", str(text))
        if url_list:
            return url_list
        else:
            return ''


if __name__ == '__main__':
    ti_instance = TiData()
    ti_instance.mergeAllDataframes()
