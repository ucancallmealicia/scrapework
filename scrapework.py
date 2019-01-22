#/usr/bin/python3
#~/anaconda3/bin/python

#A multipurpose webscraping framework

from bs4 import BeautifulSoup
import requests, csv, os, traceback

'''To-Do:

1.) Add a mkdir for output directory
2.) Add timer for running weekly
'''
#'http://findit.library.yale.edu/?f%5Baccess_restrictions_sim%5D%5B%5D=Open+With+Permission&page=2&per_page=100'
#105 pages

class Scrape():
        
    #pagelist should be a list with 4 or 5 items - multi-page structure, begin, end, step
        self.url = url
        self.directory = directory
        self.filename = filename
        self.pagelist = pagelist

    #Open a CSV in reader mode
    def opencsv(self):
        try:
            input_csv = input('Please enter path to CSV: ')
            if input_csv == 'quit':
                return
            else:
                file = open(input_csv, 'r', encoding='utf-8')
                csvin = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
                next(csvin)
                return csvin
        except FileNotFoundError:
            print('CSV not found. Please try again. Enter "quit" to exit')
            c = self.opencsv()
            return c

    #Open a CSV file in writer mode
    def opencsvout(self, output_csv=None):
        try:
            if output_csv is None:
                output_csv = input('Please enter path to output CSV: ')
            if output_csv == 'quit':
                return
            fileob = open(output_csv, 'a', encoding='utf-8', newline='')
            csvout = csv.writer(fileob)
            return (fileob, csvout)
        except Exception:
            print('Error creating outfile. Please try again. Enter "quit" to exit')
            f, c = self.opencsvout()
            return (f, c)
            
    #define a method to parse through pages
    def p_list(self):
        pl = list(range(self.pagelist[1], self.pagelist[2], self.pagelist[3]))
        return pl

    #method to download page(s) and write to file
    def get_page(self, fname=None, url=None):
        try:
            if url != None:
                gurl = requests.get(url)
            else:
                gurl = requests.get(self.url)
            if fname != None:
                output_filename = fname
            else:
                output_filename = self.filename
            if gurl.status_code == requests.codes.ok:
                data = gurl.text
                output = open(self.directory + '/' + output_filename + '.txt', 'a', encoding='utf-8')
                output.write(data)
                output.close()
            else:
                print(self.url)
                print(gurl.status_code)
        except Exception as exc:
            if url != None:
                print(url)
            else:
                print(self.url)
            print(traceback.format_exc())
    
    #actually downloads the page(s)
    def get_pages(self):
        try:
            if len(self.pagelist) == 4:
                pages = self.p_list()
                for page in pages:
                    file_name = self.filename + str(page)
                    if '{}' in self.pagelist[0]:
                        x = self.get_page(fname=file_name, url=self.url + self.pagelist[0] + str(self.pagelist[0].format(str(page), str(self.pagelist[2]))))
                    else:
                        self.get_page(fname=file_name, url=self.url + self.pagelist[0] + str(page))
            if len(self.pagelist) == 0:
                self.get_page(self.filename, self.url)
        except Exception as exc:
            print(traceback.format_exc())

    def get_value(self, user_input):
        if user_input != "no":
            return user_input

    #enter a string with whatever it is you would want in a findall    
    def parse_files(self):
        returns = []
        filelist = os.listdir(self.directory)
        tag = input('Please enter a tag or list of tags to search, or enter "no": ')
        tag_class = input('If you want to search a class, enter it here, or enter "no": ')
        attributes = input('If you want to search by attribute, enter it here (like attr_key: attr_value), or enter "no": ')
        for file in filelist:
            if file != '.DS_Store':
                openfile = open(self.directory + '/' + file, 'r', encoding='utf-8')
                soup = BeautifulSoup(openfile, 'lxml')
                #x = soup.find_all(str(maintag), class_="entry-content")
                x = soup.find_all(name=self.get_value(tag), class_=self.get_value(tag_class), attrs={self.get_value(attributes)})
                returns.append(x)
        #just return the results and you can do whatever processing you want interactively
        return returns

