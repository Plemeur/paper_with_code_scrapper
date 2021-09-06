import json
from bs4 import BeautifulSoup
import httplib2
import urllib.parse as parse
from tqdm import tqdm


client = httplib2.Http()
website_root = 'https://paperswithcode.com/'

try: 
    with open('dataset_full.json', 'r') as f:
        papers_dict = json.load(f)
except:
    with open('dataset_cleaned.json', 'r') as f:
        papers_dict = json.load(f)


for i,( paper, attributes) in enumerate(tqdm(papers_dict.items())):
    if 'tasks' in attributes.keys():
        continue

    link = attributes['link']
    status, response = client.request(parse.urljoin(website_root, link))

    soup = BeautifulSoup(response, 'html.parser')
    
    # Get tasks
    try: 
        tasks = soup.find('div', {'id':'tasks'}).findAll('span', {'class':'badge'})
        papers_dict[paper]['tasks'] = []

        for task in tasks:
            papers_dict[paper]['tasks'].append(task.find('span').text)
    except:
        pass

    # Get Abstract
    try: 
        abstract = soup.find('div', {'class': 'paper-abstract'}).find('p').text
        abstract = abstract.replace('read more', '')
        abstract = abstract.replace('...','')
        abstract = abstract.replace('\n',' ')
        papers_dict[paper]['abstract'] = abstract
    except: 
        papers_dict[paper]['abstract'] = ''

    # Get arXiv link
    try: 
        arxiv = soup.find('div', {'class': 'paper-abstract'}).find('a', {'class':'badge'}).attrs['href']
        papers_dict[paper]['arxiv'] = arxiv
    except:
        papers_dict[paper]['arxiv'] = ''

    if not (i % 1000 ):
        with open('dataset_full.json', 'w') as f:
            json.dump(papers_dict, f)

with open('dataset_full.json', 'w') as f:
    json.dump(papers_dict, f)