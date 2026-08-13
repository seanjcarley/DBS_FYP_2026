import get_report as gr
from bs4 import BeautifulSoup


def main():
    data = gr.GetReport()

    # return data
    soup = BeautifulSoup(data, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    main()