#!/usr/bin/env python
# coding: utf-8

# In[30]:


import requests
from bs4 import BeautifulSoup

URL = "http://www.fondation.org.ma/web/display_edoc/93/17"

r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')

all_scripts = soup.find_all('script')
print(all_scripts)


# In[31]:


import re
import os

tmp = str(all_scripts[4]).split("src:")
makhtuta = []
 

for full in tmp[1:]:
    each_page = str(full)
    res = re.sub(r', thumb.*',"",each_page)
    almost_clean = res.split(",{")
    link = almost_clean[0].split("\"")
    makhtuta.append(link[1])
print(len(makhtuta))
print(makhtuta[1:6])


book = "حل الرموز ومفتاح الكنوز ابن غانم"
path = str(r"C:\Users\junai\Documents\Islamic Classes\Fiqh\Manuscripts"  + "\\")
dir = ''.join([path, book, "\\"])

print(dir)
os.mkdir(dir)


# In[32]:


for page_url in makhtuta:
    print(page_url)
 
    filename = ''.join([dir, page_url.split('/')[-1]])
    print(filename)

    r = requests.get(page_url, allow_redirects=True)

    open(filename, 'wb').write(r.content)


# In[ ]:




