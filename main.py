import get_report as gr
import process_report as pr
from datetime import datetime as dt


def main():
    # get the current date
    today = dt.now()

    # set the max search terms so that future dates will not be submitted
    max_year = today.year
    max_month = today.month
    max_day = today.day

    max_search_date = dt(max_year, max_month, max_day)
    min_search_date = dt(2017, 6, 1)  # the oldest data is from this date

    def format_date(date_type):
        ''' extract day, month, year from date provided in DD/MM/YYYY format '''

        # ensuring that the end date submitted by the user is not before the
        # start data already submitted
        if date_type == 'end':
            search_date = dt(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
        else:
            search_date = min_search_date

        valid = False

        while not valid:
            try:
                # get the date from the user
                date = input(f'Please enter the {date_type} date in the DD/MM/YYYY format: ')
                year, month, day = int(date[6:]), int(date[3:5]), int(date[0:2])

                f_date = dt(year, month, day)

                # make sure that the user supplied date is on or after the
                # earliest date that data is available for and not a future 
                # date
                if search_date <= f_date <= max_search_date:
                    f_date = dt(year, month, day)
                    valid = True
                else:
                    # if it is advise the user that the date is not within the
                    # allowed date range and ask to resubmit the date
                    print(f'{date} is not within the range {search_date.strftime("%d/%m/%Y")} - {max_search_date.strftime("%d/%m/%Y")}')
            except ValueError as e:
                # capture exception if invalid date format is entered and ask
                # the user to reenter the date in the correct format
                print(f'The date provided {date} was not in the correct DD/MM/YYYY format!')
                print('Please reenter the date!')
            
        return f_date.strftime("%Y-%m-%d")

    # ########################################################################
    # request the date range from the user
    print('Data is available from June 2017 to today...')
    start_date = format_date('start')
    end_date = format_date('end')
    # ########################################################################

    # print(start_date, end_date)  # used for testing
    
    # create scrape object
    data1 = gr.GetReport(start_date, end_date).get_report_data()
    # data2 = gr.GetReport('2023-02-01', '2023-02-28').get_report_data()
    # print(data)  # used to test scrape

    # create report processing object
    pr.ProcessReport(data1).make_soup()
    # pr.ProcessReport().make_soup()  # to be used for testing using local html file

if __name__ == '__main__':
    main()
