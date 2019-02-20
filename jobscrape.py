#!/usr/bin/python3
#~/anaconda3/bin/python

from bs4 import BeautifulSoup
import requests, csv, os, traceback, logging, sys
from datetime import datetime
import scrapework

''' Job Sites to Scrape

ArchivesGig: https://archivesgig.com/; https://archivesgig.com/page/1/
SAA Job Board: https://careers.archivists.org/jobs/
ALA Job Board: https://joblist.ala.org/jobs/; https://joblist.ala.org/jobs/?str=26&max=25&vnet=0&long=1
RBMS Jobs: https://rbms.info/blog/category/news-events/jobs-positions/; https://rbms.info/blog/category/news-events/jobs-positions/page/2/
AASLH: https://jobs.aaslh.org/jobs/?str=1&max=25&long=1&vnet=0; https://jobs.aaslh.org/jobs/?str=26&max=25&long=1&vnet=0

'''

def error_log(filepath=None):
    if sys.platform == "win32":
        if filepath == None:
            logger = '\\Windows\\Temp\\error_log.log'
        else:
            logger = filepath
    else:
        if filepath == None:
            logger = '/tmp/error_log.log'
        else:
            logger = filepath
    logging.basicConfig(filename=logger, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    return logger

error_log
root_directory_path = '/Users/aliciadetelich/Dropbox/git/scrapework/output/'
today = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
directory_path = root_directory_path + today
os.mkdir(directory_path)
error_log(filepath=directory_path + '/log.log')

#Add data for SAA jobs site...
website_data = [{'filename_convention': 'archivesgig', 'url_input': 'https://archivesgig.com', 
				'page_data': ['/page/', 1, 6, 1]}, 
				{'filename_convention': 'saa_jobs', 'url_input': 'https://careers.archivists.org/jobs', 
				'page_data': ['/?page=', 1, 6, 1], 'baseurl': 'https://careers.archivists.org'},
				{'filename_convention': 'ala_jobs', 'url_input': 'https://joblist.ala.org/jobs',
				'page_data': ['/?str={}&max={}&vnet=0&long=1', 1, 150, 25], 'baseurl': 'https://joblist.ala.org'}, 
				{'filename_convention': 'rbms_jobs', 'url_input': 'https://rbms.info/blog/category/news-events/jobs-positions', 
				'page_data': ['/page/', 1, 5, 1]}, 
				{'filename_convention': 'aaslh', 'url_input': 'https://jobs.aaslh.org/jobs', 
				'page_data': ['/?str={}&max={}&long=1&vnet=0', 1, 150, 25], 'baseurl': 'https://jobs.aaslh.org'}]

#Reads in a list of URLs to be excluded from the scrape
exclusion_file = open('exclusions.txt', 'r', encoding='utf-8').read()
exclusions = exclusion_file.split(', ')

for data_bit in website_data:
	s = scrapework.Scrape(data_bit['url_input'], directory_path, data_bit['filename_convention'], data_bit['page_data'])
	if data_bit['page_data'][0] != '':
		s.get_pages()
	else:
		s.get_page()

fileobject, csvoutfile = s.opencsvout(output_csv=directory_path + '/urls.csv')
csvoutfile.writerow(['uri'])

def form_link(l, website_data, fname):
	if l.startswith('/job'):
		for d in website_data:
			if d['filename_convention'] in fname:
				l = d['baseurl'] + link
	return l

compiled_data = s.parse_files(tag='a', tag_class='no', attributes='no')
data = []
for page, fname in compiled_data:
	for tag in page:
		try:
			link = tag['href']
			if 'archivesgig'not in link:
				if link not in exclusions:
					if link.startswith('/job'):
						link = form_link(link, website_data, fname)
					if [link] not in data:
						data.append([link])
		except KeyError:
			logging.exception('error: ')
			logging.debug('key error: ' + str(tag))

csvoutfile.writerows(data)
fileobject.close()

csvfile = s.opencsv(input_csv=directory_path + '/urls.csv')

for i, row in enumerate(csvfile, 1):
	job_posting = row[0]
	s.get_page(fname='jobs' + str(i), url=job_posting)

'''TO DO
1.) Pull data from job posting pages
2.) Logging for classes - i.e. 403 errors; just prints to console now
'''
