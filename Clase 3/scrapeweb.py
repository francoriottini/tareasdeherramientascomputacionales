# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import csv
from bs4 import BeautifulSoup as bs

url = requests.get("https://www.top500.org/lists/hpcg/list/2018/06/")
soup = bs(url.content, 'html.parser')

filename = "computerRank10.csv"
csv_writer = csv.writer(open(filename, 'w'))


for tr in soup.find_all("tr"):
    data = []
    # for headers ( entered only once - the first time - )
    for th in tr.find_all("th"):
        data.append(th.text)
    if data:
        print("Inserting headers : {}".format(','.join(data)))
        csv_writer.writerow(data)
        continue

    for td in tr.find_all("td"):
        if td.a:
            data.append(td.a.text.strip())
        else:
            data.append(td.text.strip())
    if data:
        print("Inserting data: {}".format(','.join(data)))
        csv_writer.writerow(data)
        
        
import csv
import requests
from bs4 import BeautifulSoup

link = "https://www.top500.org/lists/top500/list/2018/06/?page={}"

def get_data(link):
    for url in [link.format(page) for page in range(1,6)]:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"lxml")

        for items in soup.select("table.table tr"):
            td = [item.get_text(strip=True) for item in items.select("th,td")]
            writer.writerow(td)

if __name__ == '__main__':
    with open("tabularitem.csv","w",newline="") as infile: #if encoding issue comes up then replace with ('tabularitem.csv', 'w', newline="", encoding="utf-8")
        writer = csv.writer(infile)
        get_data(link)
