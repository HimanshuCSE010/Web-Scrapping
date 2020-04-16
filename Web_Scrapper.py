"""
Web Scrapping project on website (www.allsides.com) 
Getting all data from a table and and converting to pandas dataframe
"""

# importing the required libraries

# for making request to get web page
import requests 
# for pasing html or xml
from bs4 import BeautifulSoup
# for sleeping progrram 
from time import sleep
# for showing progress while looping
from tqdm import tqdm   # for jupyter use -- from tqdm import tqdm_notebook
# for making deep copy
from copy import deepcopy
# for storing data
import json
# for getting realative path to save file in current folder
import os 

# save in html 
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

# read from html 
def read_html(path):
    with open(path, 'rb') as f:
        return f.read()

# to replicate aggregance as per web site data
def get_agreeance_text(ratio):
    if ratio > 3: return "absolutely agrees"
    elif 2 < ratio <= 3: return "strongly agrees"
    elif 1.5 < ratio <= 2: return "agrees"
    elif 1 < ratio <= 1.5: return "somewhat agrees"
    elif ratio == 1: return "neutral"
    elif 0.67 < ratio < 1: return "somewhat disagrees"
    elif 0.5 < ratio <= 0.67: return "disagrees"
    elif 0.33 < ratio <= 0.5: return "strongly disagrees"
    elif ratio <= 0.33: return "absolutely disagrees"
    else: return None

# list of all pages we want to parse through
pages = [
    'https://www.allsides.com/media-bias/media-bias-ratings',
    'https://www.allsides.com/media-bias/media-bias-ratings?page=1',
    # 'https://www.allsides.com/media-bias/media-bias-ratings?page=2'
]

# list for data collection 
data= []

for page in pages:
    # placing get request
    r = requests.get(page)

    # creating BS4 object by passing html content and type of parser
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # selecting elements to get data
    # selecting tables and its rows
    if soup.select('tbody tr') is not None:
        rows = soup.select('tbody tr')

        # for each row specific obtain data
        for row in rows:
            d = dict()
            # .text get all text inside element, strip shaves off extra whitespace,
            d['name'] = row.select_one('.source-title').text.strip()

            # access an attribute (href) of the element using brackets, like dict of python
            d['allsides_page'] = 'https://www.allsides.com' + row.select_one('.source-title a')['href']

            # getting bias rating 
            d['bias'] = row.select_one('.views-field-field-bias-image a')['href'].split('/')[-1]

            # getting comunity feedback data
            d['agree'] = int(row.select_one('.agree').text)
            d['disagree'] = int(row.select_one('.disagree').text)
            d['agree_ratio'] = d['agree'] / d['disagree']

            # classification based on  agree ratio
            d['agreeance_text'] = get_agreeance_text(d['agree_ratio'])

            data.append(d)
        # make another request after 10s as it is the crawl time given in robot.txt    
        sleep(1)

# pass the iterable to tqdm
for d in tqdm(data):         
    # get request from main page of news website over allsides.com
    r = requests.get(d['allsides_page'])
    soup = BeautifulSoup(r.content, 'html.parser')
    
    try:
        # try to get actual web address for that news channel
        website = soup.select_one('.www')['href']
        # if found then store in dictionary
        d['website'] = website
    except TypeError:
        pass
    
    sleep(1)

# saving data
seperator = os.sep
path = __file__.split(seperator)[:-1]
path = seperator.join(path) + seperator + 'allsides.json'

with open(path,'w') as f:
    json.dump(data, f)

with open(path,'r') as f:
    data = json.load(f)

