#Import libraries for TinyURL
from __future__ import with_statement                                                         
  
import contextlib 
  
try: 
    from urllib.parse import urlencode           
  
except ImportError: 
    from urllib import urlencode 
  
try: 
    from urllib.request import urlopen 
  
except ImportError: 
    from urllib2 import urlopen 
  
import sys

#Import libraries for scraping
import requests
from bs4 import BeautifulSoup


def make_tiny(url): 
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))    
    with contextlib.closing(urlopen(request_url)) as response:                       
        return response.read().decode('utf-8 ')

def main():                                                                 
    for tinyurl in map(make_tiny, sys.argv[1:]):                     
        print(tinyurl) 
  
if __name__ == '__main__': 
    main()


#Start of program
job = input("Job:")
location = input("Location:")
print()


#URL order is Monster, Indeed
sites = ['Monster', 'Indeed']
URLs = ['https://www.monster.com/jobs/search/?q={0}&where={1}'.format(job, location), 'https://www.indeed.co.uk/jobs?q={0}&l={1}'.format(job, location)]
resultContainers = ['ResultsContainer', 'resultsCol']
job_elem_type = ['section', 'div']
job_elem_class = ['card-content', 'jobsearch-SerpJobCard unifiedRow row result']
title_elem_type = ['h2', 'h2']
title_elem_class = ['title', 'title']
company_elem_type = ['div', 'span']
company_elem_class = ['company', 'company']
location_elem_type = ['div', 'div']
location_elem_class = ['location', 'location accessible-contrast-color-location']



#Scrape the dataa for each site and write to file
resultsNum = 0
filename = 'jobs.csv'
f = open(filename, 'w')
headers = 'title, company, location, website, link\n'
f.write(headers)
for i in range(len(URLs)):
    page = requests.get(URLs[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id=f'{resultContainers[i]}')
    job_elems = results.find_all(f'{job_elem_type[i]}', class_=f'{job_elem_class[i]}')
    resultsNum = resultsNum + len(job_elems)
    
    for job_elem in job_elems:
        title_elem = job_elem.find(f'{title_elem_type[i]}', class_=f'{title_elem_class[i]}')
        company_elem = job_elem.find(f'{company_elem_type[i]}', class_=f'{company_elem_class[i]}')
        location_elem = job_elem.find(f'{location_elem_type[i]}', class_=f'{location_elem_class[i]}')
        if None in (title_elem, company_elem, location_elem):
            continue
        title = title_elem.text.strip()
        company = company_elem.text.strip()
        location = location_elem.text.strip()
        link = title_elem.find('a')['href']
        if i==1:
            link = f'https://www.indeed.co.uk{link}'
        link = make_tiny(link)
        print(f'Title: {title}')
        print(f'Company: {company}')
        print(f'Location: {location}')
        print(f'Website: {sites[i]}')
        print(f'Link: {link}\n')
        f.write(title.replace(",", "-") + "," + company.replace(",", "-") + "," + location.replace(",", "-") + "," + sites[i] + "," + link + "\n")
    count=+1
f.close()
print(f'{resultsNum} results found')
input('Press ENTER to exit')
