#!/usr/bin/env python
# coding: utf-8

# # Amazon Web Scraper

# In[6]:


import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    search_term = search_term.replace(' ','+')
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    # add term query to url
    url = template.format(search_term)
    # add page
    url += '&page{}'
    return url
# url = get_url(str(input(Enter the search :)))
# url = get_url('ultrawide monitor')

def extract_record(item):
    # """Extract and return data from a single record"""

    #description and link
    atag = item.h2.a
    item_des = atag.text.strip()
    item_link = 'https://www.amazon.in' + atag.get('href')

    #price
    try:
        buy_price = item.find('span', 'a-price')
        item_buy_price = buy_price.find('span', 'a-offscreen').text
        og_price = item.find('span', 'a-price a-text-price')
        item_og_price = og_price.find('span', 'a-offscreen').text
    except AttributeError:
        return

    #rating and review
    try:
        rating = item.i.text
        reviews = item.find('span', 'a-size-base').text
    except:
        rating =''
        reviews =''

    result = (item_des,item_buy_price,item_og_price,rating,reviews,item_link)
    return result

def main(search_term):
    PATH = 'C:\Program Files\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    url = 'https://www.amazon.in/'
    driver.get(url)

    extracted_record = []
    url = get_url(search_term)
    
    for page in range (1,21):
        driver.get(url.format(page))
    
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all('div',{'data-component-type':'s-search-result'})
    for item in results:
        record = extract_record(item)
        if record:                              #if present
            extracted_record.append(record)
            
    driver.close()    
    
    #saving data to csv file
    with open('results.csv','w',newline='',encoding='utf=8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Buy Price','Original Price','Rating','Reviews','Link'])
        writer.writerows(extracted_record)


# In[9]:


#this is a default search term you can enter your own search by uncommenting the below code

main('ultrawide monitor')

# user=input()
# main(user)


# In[ ]:




