from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import csv
import re

class ScrapCryptolaemus():
    def __init__(self):
        page = requests.get("https://paste.cryptolaemus.com/")
        if page.status_code == 200:
            self.soup = BeautifulSoup(page.content, 'html.parser')

    def scrapLinksFilter(self):
        upto = datetime.now() - timedelta(days = 90)
        if self.soup:
            filtered_list = []
            link_list = self.soup.find_all('h4')
            for link in link_list:
                tags = list(link.children)
                date = datetime.strptime(tags[0].get_text(), '%d %B %Y')
                href = tags[2]['href']
                if date > upto:
                    filtered_list.append((date, href))
        return filtered_list

    def getData(self, links):
        base = 'https://paste.cryptolaemus.com'
        with open('cryptolaemusdata.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['date', 'link', 'ip_domain_url list', 'user'])
        for link in links:
            final_list = []
            url = base + link[1]
            page = requests.get(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                data = soup.find_all('code')
                for item in data:
                    txt = item.get_text()
                    lst = txt.split('\n')
                    lst = [x for x in lst if x != '']
                    lst = list(set(lst))
                    comp = re.compile(r'(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d{1,5})?$)|(^(?:(?:http?|https):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+$)|(^[0-9a-f]{64}$)')
                    lst = [x for x in lst if comp.search(x) is not None and not x.startswith('https://twitter.com/') and not x.startswith('https://pastebin.com/')]
                    if lst:
                        final_list.append(lst)
            with open('cryptolaemusdata.csv', mode='a') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([link[0].strftime('%d-%B-%Y'), url, final_list, '@cryptolaemus'])



def main():
    scrap_obj = ScrapCryptolaemus()
    links = scrap_obj.scrapLinksFilter()
    scrap_obj.getData(links)


if __name__ == '__main__':
    main()
