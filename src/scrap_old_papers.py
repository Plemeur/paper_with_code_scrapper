from selenium import webdriver
from bs4 import BeautifulSoup
import json
import urllib
from time import sleep

driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
website_root = 'https://paperswithcode.com/'


papers_dict = {}
driver.get(urllib.parse.urljoin(website_root,'methods'))
screen_height=driver.execute_script('return window.screen.height;')

soup = BeautifulSoup(driver.page_source, 'html.parser')
areas = soup.findAll('h4')

with open('dataset.json', 'r') as f:
    papers_dict = json.load(f)

done_methods = set()
for p, d in papers_dict.items():
    for m in d['method']:
        done_methods.add(m)



for area in areas:
    ref = area.find('a').attrs['href']
    area_name = ref.split('/')[-1]
    print(f'Now scrapping Area : {area_name}')
    driver.get(urllib.parse.urljoin(website_root, ref))
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    categories = soup.findAll('h2')
    

    for category in categories:
        ref = category.find('a').attrs['href']
        category_name = ref.split('/')[-1]
        print(f'    Now scrapping Category : {category_name}')
        driver.get(urllib.parse.urljoin(website_root, ref))
        sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        methods = soup.findAll("div", {"class": "method-image"})

        for method in methods:
            ref = method.find('a').attrs['href']
            method_name = ref.split('/')[-1]
            if method_name in done_methods:
                continue

            print(f'\t\t Now Scrapping Method : {method_name}')
            driver.get(urllib.parse.urljoin(website_root, ref))
            sleep(1)
      
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            papers = soup.findAll("div", {"class": "black-links"})
            
            sleep(2)
            for paper in papers:
                link_container = paper.find('a')
                entry = papers_dict.get(link_container.text, {})
                entry['link'] = entry.get('link', link_container.attrs['href'])
                entry['area'] = entry.get('area', [])+[area_name]
                entry['method'] = entry.get('method', []) + [method_name]
                entry['category'] = entry.get('category', []) + [category_name]
                papers_dict[link_container.text] = entry

            try:
                next_button = driver.find_element_by_id('datatable-papers_next')
                driver.execute_script('arguments[0].scrollIntoView(true);', next_button)
                sleep(2)
            except:
                continue

            next_button.click()
            sleep(1)

            while True : 
                try : 
                    next_button.click()
                    break
                except:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    papers = soup.findAll("div", {"class": "black-links"})
                    for paper in papers:
                        link_container = paper.find('a')
                        entry = papers_dict.get(link_container.text, {})
                        entry['link'] = entry.get('link', link_container.attrs['href'])
                        entry['area'] = entry.get('area', []) + [area_name]
                        entry['method'] = entry.get('method', [])+ [method_name]
                        entry['category'] = entry.get('category', []) + [category_name]
                        papers_dict[link_container.text] = entry
                    next_button = driver.find_element_by_id('datatable-papers_next')
                    next_button.click()
                    sleep(2)
                    

            with open('dataset.json', 'w') as f:
                json.dump(papers_dict, f)
