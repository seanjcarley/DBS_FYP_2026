import get_report as gr
from bs4 import BeautifulSoup


def main():
    data1 = gr.GetReport('2023-01-01', '2023-01-31').get_report_data()
    # data2 = gr.GetReport('2023-02-01', '2023-02-28').get_report_data()
    # print(data)

    # return data
    soup = BeautifulSoup(data1, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    main()