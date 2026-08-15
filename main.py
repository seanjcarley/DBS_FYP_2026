import get_report as gr
import process_report as pr
from bs4 import BeautifulSoup
import datetime as d
from datetime import datetime as dt


def main():
    today = dt.now()
    max_year = today.year
    max_month = today.month
    max_day = today.day
    # max_hour = today.hour

    max_search_date = dt(max_year, max_month, max_day)
    min_search_date = dt(2017, 6, 1)

    def format_date(date):
        ''' extract day, month, year from date provided in DD/MM/YYYY format '''
        try:
            year, month, day = int(date[6:]), int(date[3:5]), int(date[0:2])
            
            date = dt(year, month, day)

            if (today < date) or (date <  min_search_date):
                revised_date = (f'The date provided is invalid. Please enter date between 01/06/2017 and {str(today.strftime("%d/%m/%Y"))}: ')
                format_date(revised_date)
            
            return date

        except ValueError as e:
            # print(e)
            revised_date = input(f'The date was not provided in the correct format. Please enter the date in DD/MM/YYY format: ')


    print('Data is available from June 2017 to today...')
    start_date = input('Please enter the start date in the DD/MM/YYYY format: ')
    st_date = format_date(start_date)
    end_date = input('Please enter the end date in the DD/MM/YYYY format: ')
    ed_date = format_date(end_date)

    print(st_date, ed_date)
    


    # data1 = gr.GetReport('2023-01-01', '2023-01-31').get_report_data()
    # data2 = gr.GetReport('2023-02-01', '2023-02-28').get_report_data()
    # print(data)

    # return data
    # soup = BeautifulSoup(data1, 'html.parser')
    # print(soup.prettify())

    # pr.ProcessReport(data1).make_soup()

if __name__ == '__main__':
    main()