from bs4 import BeautifulSoup
import time as t
import datetime as dt

class ProcessReport:

    def __init__ (self, report):
        self.report = report


    def make_soup(self):
        soup = BeautifulSoup(self.report, 'html.parser')

        for item in soup.select('tbody tr td'):
            print(item)
            
            
