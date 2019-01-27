#import statements
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen
import wget
import pandas as pd
import zipfile
import json
import redis
import sys
#setting the url and initializing beautiful soup
ss = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx?utm_campaign=website&utm_source=sendgrid.com&utm_medium=email"
soup = bs(urlopen(ss), features = "lxml")

#extracting and downloading zip
zipp = soup.find("li", {"id" : "ContentPlaceHolder1_liZip"})
links = zipp.find('a', href=True)
dl_file = wget.download(links['href'])
filename = dl_file.split("_")
zf = zipfile.ZipFile(dl_file) 

#taking into a dataframe and finally into a redis hashmap
df = pd.read_csv(zf.open(filename[0]+".CSV"))
#print df.head()
df["GAIN"] = ((df["CLOSE"] - df["OPEN"]) / df["OPEN"]) * 100

print df.head()
print df.keys()
df = df.sort_values(by=['GAIN'], ascending = False)
names = df['SC_NAME']
names =[name.strip() for name in names]
conn = redis.Redis('localhost')
for index, row in df.iterrows():
	fname = row["SC_NAME"].strip()
	conn.hmset(fname, { "code" : row["SC_CODE"], "open" : row["OPEN"], "low" : row["LOW"], "close" : row["CLOSE"], "high": row["HIGH"], "gain" : "%.2f"%row["GAIN"]})



toptennames = names[0:10]
conn.delete("top10namekeys")
conn.rpush('top10namekeys', *toptennames)
elements = conn.lrange( "top10namekeys", 0, -1 )
print elements
