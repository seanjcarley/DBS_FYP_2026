from bs4 import BeautifulSoup
import time as t
from datetime import datetime as dt

class ProcessReport:

    # def __init__ (self, report):
        # self.report = report
    def __init__ (self):
        self.report = open('test.html')
        self.months = {'january': 1, 'february': 2, 'march': 3, 
                    'april': 4, 'may': 5, 'june': 6, 
                    'july': 7, 'august': 8, 'september': 9, 
                    'october': 10, 'november': 11, 'december': 12}
        self.events = {'qc failure ': 1, 'qc outlier': 2, 'qc atypical': 3,
                       'events': 4, 'special': 5, 'holiday': 6, 
                       'offline': 7, 'oeekends and defined holidays': 8, 
                       'holiday-affected days': 9}


    def make_soup(self):
        soup = BeautifulSoup(self.report, 'html.parser')

        mbk, car, lgv, bus, hgr, hga, cvn, ivd = [], [], [], [], [], [], [], []

        for tr in soup.select('tbody tr'):
            entry = []
            for td in tr.select('td'):
                if not td.has_attr('class'):
                    if td.has_attr('rowspan'):
                        if int(str(td).split('"')[1]) == 16:
                            td_str = str(td).replace('<td rowspan="16">', '').replace('</td>', '')
                            date_str =  td_str.split(' ')
                            month_str = date_str[2].lower()
                            date = dt(int(date_str[3]), self.months[month_str], int(date_str[1]))
                            # print(date.strftime("%Y-%m-%d"))
                            entry.append(date)
                
                if td.has_attr('class'):
                    # print(td.attrs['class'], td.attrs['data-a'])
                    values = td.attrs['data-a'].split(',')
                    if len(td.attrs['class']) == 0:
                        entry.append(0)
                    else:
                        event = self.events[td.attrs['class'][0]]
                    entry.append(event, values[0], values[2], values[3])

            print(entry)



                



                    
                
            
            
