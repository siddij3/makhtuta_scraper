#!/usr/bin/env python
# coding: utf-8

# In[26]:


def get_requests(title, makhtuta):

    return requests.get(title), requests.get(makhtuta)

def find_author_title(soup):

    tag_book = soup.find_all("h1")
    pattern = "\>(.*?)\<"
    book = re.search(pattern, str(tag_book[0])).group(1)

    tag_author = soup.find_all("td", "text-center col-6")
    pattern = "\>(.*?)\<"
    author = re.search(pattern, str(tag_author[0])).group(1)

    book_binding = book + " " + author

    return book_binding

def make_folder(path, book_binding):


    book_binding = remove_multiple_strings(book_binding)

    x = datetime.datetime.now()
    manuscript_id = ''.join([x.strftime("%d"), x.strftime("%b"), x.strftime("%y"), x.strftime("%H"), x.strftime("%M")])


    directory = ''.join([path,  manuscript_id, "-", book_binding, "\\"])
    print(manuscript_id, directory)

    os.makedirs(directory)
    print("Duplicate book")

    return directory


# In[2]:


def compile_pages(page_scripts):

    tmp = str(page_scripts[4]).split("src:")
    makhtuta = []

    for full in tmp[1:]:
        each_page = str(full)
        res = re.sub(r', thumb.*',"",each_page)
        almost_clean = res.split(",{")
        link = almost_clean[0].split("\"")
        makhtuta.append(link[1])

    print("length of makhtuta", len(makhtuta))
    return makhtuta


# In[3]:


def download_pages(makhtuta, directory):

    for page_url in makhtuta:

        filename = ''.join([directory, page_url.split('/')[-1]])

        r = requests.get(page_url, allow_redirects=True)

        open(filename, 'wb').write(r.content)


# In[27]:


def remove_multiple_strings(cur_file):

    original_string = cur_file
    characters_to_remove = "/\\:*?\"<>|"

    if any(c in characters_to_remove for c in original_string):
        print("yes, there are stupid characters")
        pattern = "[" + characters_to_remove + "]"
        return re.sub(pattern, "", original_string)

    print("no stupid characters")
    return original_string


    #replace_list = ['/', '\\', ':', '*', '?', '\"', '<', '>', '|', '\"', ]
    #print(replace_list)

    #for cur_word in replace_list:
     #   print(cur_word)
      #  cur_file = cur_file.replace(cur_word, '')
    #return cur_file


# In[ ]:


import requests
from bs4 import BeautifulSoup
import re
import os
import datetime

path = str(r"."  + "\\")
pages = [1733,1729,1880,1912,1905,1937]

for i in pages:

    URL_title = "http://www.fondation.org.ma/web/affichage_numerics/{}/17".format(i)
    URL_makhtuta = "http://www.fondation.org.ma/web/display_edoc/{}/17".format(i)

    r_title, r_makhtuta = get_requests(URL_title, URL_makhtuta)

    soup_title = BeautifulSoup(r_title.text, 'html.parser')
    soup_makhtuta = BeautifulSoup(r_makhtuta.text, 'html.parser')

    #get the book title and author
    book_binding = find_author_title(soup_title)

    # create directory
    directory = make_folder(path, book_binding)
    print(directory)

    # get all the links

    all_scripts = soup_makhtuta.find_all('script')
    makhtuta = compile_pages(all_scripts)

    #Putting all the files into the folder
    download_pages(makhtuta, directory)


# dl


# In[ ]:





# In[ ]:
