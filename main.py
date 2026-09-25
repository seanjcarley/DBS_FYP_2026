#!/usr/bin/python3
from data_scrape import data_scrape
from get_prediction import get_prediction

def main():

    print(f'Welcome to the Traffic Volume Predictor')

    def get_choice():
        print('\nWhat would you like to do:')
        print('1. Get the latest data...')
        print('2. Get a prediction...')
        print('3. Exit...')
        choice  = int(input('Please enter the number of your choice: '))

        return choice

    choice = get_choice()

    while 0 < choice < 3:
        # print(f'Current choice is: {choice}')
        match choice:
            case 1:
                data_scrape()
                choice = get_choice()
                # print(choice)
            case 2:
                get_prediction()
                choice = get_choice()
                # print(choice)


if __name__ =='__main__':
    main()
