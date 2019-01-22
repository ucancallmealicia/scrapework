#/usr/bin/python3
#~/anaconda3/bin/python

from bs4 import BeautifulSoup
import requests, csv, os, traceback, logging
from scrapework import Scrape

''' Job Sites to Scrape

ArchivesGig: https://archivesgig.com/; https://archivesgig.com/page/1/
SAA Job Board: https://careers.archivists.org/jobs/
ALA Job Board: https://joblist.ala.org/jobs/; https://joblist.ala.org/jobs/?str=26&max=25&vnet=0&long=1
RBMS Jobs: https://rbms.info/blog/category/news-events/jobs-positions/; https://rbms.info/blog/category/news-events/jobs-positions/page/2/
AASLH: https://jobs.aaslh.org/jobs/?str=1&max=25&long=1&vnet=0; https://jobs.aaslh.org/jobs/?str=26&max=25&long=1&vnet=0

'''

directory_path = input('Please enter path to output directory: ')

#Add data for SAA jobs site...
website_data = [{'filename_convention': 'archivesgig', 'url_input': 'https://archivesgig.com', 
				'page_data': ['/page/', 1, 50, 1]}, 
				{'filename_convention': 'saa_jobs', 'url_input': 'https://careers.archivists.org/jobs', 
				'page_data': ['', '', '', '']},
				{'filename_convention': 'ala_jobs', 'url_input': 'https://joblist.ala.org/jobs', 
				'page_data': ['/?str={}&max={}&vnet=0&long=1', 1, 250, 25]}, 
				{'filename_convention': 'rbms_jobs', 'url_input': 'https://rbms.info/blog/category/news-events/jobs-positions', 
				'page_data': ['/page/', 1, 50, 1]}, 
				{'filename_convention': 'aaslh', 'url_input': 'https://jobs.aaslh.org/jobs', 
				'page_data': ['/?str={}&max={}&long=1&vnet=0', 1, 250, 25]}]

#Reads in a list of URLs to be excluded from the scrape
exclusion_file = open('exclusions.txt', 'r', encoding='utf-8').read()
exclusions = exclusion_file.split(', ')

for data_bit in website_data:
	s = Scrape(data_bit['url_input'], directory_path, data_bit['filename_convention'], data_bit['page_data'][0], 
		data_bit['page_data'][1], data_bit['page_data'][2], data_bit['page_data'][3])
	if data_bit['page_data'][0] != '':
		s.get_pages()
	else:
		s.get_page()

fileobject, csvoutfile = s.opencsvout()
csvoutfile.writerow(['uri'])

compiled_data = s.parse_files()
data = []
for page in compiled_data:
	for tag in page:
		try:
			link = tag['href']
			if 'archivesgig'not in link:
				if link not in exclusions:
					if [link] not in data:
						data.append([link])
		except KeyError:
			print('key error: ' + str(tag))

csvoutfile.writerows(data)
fileobject.close()

csvfile = s.opencsv()

for i, row in enumerate(csvfile, 1):
	job_posting = row[0]
	s.get_page(fname='jobs' + str(i), url=job_posting)

'''TO DO
1.) Find way to append base URL to /jobs hrefs
2.) Pull data from job posting pages
'''
