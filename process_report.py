#!/usr/bin/python3

from bs4 import BeautifulSoup

class ProcessReport:
    ''' 
        process html from get_report an parse it using Beautiful Soup to create 
        data to be entered to data base so that there is a local copy rather 
        than repeatedly accessing the website
    '''

    def __init__ (self, report):  # omit report for testing
        self.report = report  # use for testing open('test.html')
        # dictionary to map string to int for the months
        self.months = {'january': 1, 'february': 2, 'march': 3, 
                    'april': 4, 'may': 5, 'june': 6, 
                    'july': 7, 'august': 8, 'september': 9, 
                    'october': 10, 'november': 11, 'december': 12}
        # dictionary to map string to int for the events that could impact volumes
        self.events = {'qc-fail': 1, 'qc-atypical': 2, 'qc-outlier': 3,
                       'road-event': 4, 'special-event': 5, 'holiday': 6, 
                       'offline': 7, 'weekend': 8, 'holiday-affected days': 9}
        # dictionary to map string to int for the days
        self.days = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 
                     'friday': 5, 'saturday': 6, 'sunday':7}


    def make_soup(self):
        ''' 
            take the html from get_report.py to prepare it to be added to the 
            database 
        '''
        soup = BeautifulSoup(self.report, 'html.parser')  # create a BeautifulSoup object

        events = []

        # the data to be used is in the Table Body element on the page
        # each table row contains a different vehicle class for each day and direction
        for tr in soup.select('tbody tr'):  
            for td in tr.select('td'):
                # the td element that has a rowspan of 16 has the date
                # the below if statement checks if the current td element and
                # if it has a rowspan of 16 it retrieves the data
                if (td.has_attr('rowspan')) and (
                    int(str(td).split('"')[1]) == 16):
                    td_str = str(td).replace(
                        '<td rowspan="16">', '').replace('</td>', '')
                    date_str =  td_str.split(' ')
                    year = int(date_str[3])
                    month = self.months[date_str[2].lower()]
                    day = int(date_str[1])
                    dow = self.days[date_str[0].lower()]

                # the td elements that have class and data-a attributes contain
                # the count for that specific direction, hour, day, vehicle 
                # class
                if (td.has_attr('class')) and (td.has_attr('data-a')):
                    td_str = str(td).split('"')
                    if td_str[1] == '':
                        # week days with no event have a class that is 
                        # interpreted as an empty string, so to avoid having an 
                        # empty string as a key in the dict, just assign int(0)
                        # to the list
                        event_class = 0
                    else:
                        # check the events dict for the int value to represent
                        # the event, change to lowercase to match the key
                        event_class = self.events[td_str[1].lower()]
                    data_a = td_str[3].split(',')  # split the data-a attr
                    direction = int(data_a[0])
                    hour = int(data_a[2])
                    vehicle_class = int(data_a[3])
                    # extract the vehicle count for the particular hour
                    vehicle_count = int(
                        td_str[4].replace('>', '').replace('</td', ''))

                    # add the processed data to the events list to be used to 
                    # add the data to the database
                    events.append([year, month, day, dow, hour, event_class, 
                                   direction, vehicle_class, vehicle_count])

        return events
