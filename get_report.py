from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logging
import log_to_file as ltf

from datetime import date as d
from time import strftime, gmtime 

LOGGER = logging.getLogger(__name__)
TODAY = str(strftime('%Y-%m-%d', gmtime()))

class GetReport:
    ''' Using selenium, this class navigates to the required url and returns 
        the required html to be processed to get the data requied '''

    screenshot_dir = ltf.create_log()

    # add to log
    ltf.write_to_log(
        LOGGER, 
        'INFO', 
        f'Started: {str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))}\n')

    def __init__ (self, start_date=TODAY, end_date=TODAY):
        self.url = "https://trafficdata.tii.ie/"
        self.st_date = start_date  # start date 
        self.ed_date = end_date  # end date

        # options to be used in setting up web driver
        self.options = Options()

        # add options to be used with web driver
        # self.options.add_argument('--headless=new')  # enable headless mode (browser not shown on screen)
        self.options.add_argument('--window-size=1920,1080')  # set window size to resemble desktop screen
        self.options.enable_bidi = True

        # create the web driver
        self.driver = webdriver.Chrome(options=self.options)  # include the options
        self.driver.get(self.url)  # create session and navigate to website

        # ActionChains allow interactions (i.e. mouse movement, click, etc...) 
        # to be queued up allowing control over how the actions are performed
        self.action = ActionChains(self.driver)

        # allows page to be polled until condition is met or timeout is 
        # exceeded, which ever comes first
        self.wdw = WebDriverWait(self.driver, 10)

        # get report data
        self.get_report_data()

    def save_screenshot(self, title):
        ''' save screen shot'''
        ltf.write_to_log(
            LOGGER,
            'INFO',
            f'Screenshot {title}.png saved to screenshots folder!\n'
        )
        self.driver.save_screenshot(f'{self.screenshot_dir}{title}.png')


    def driver_quit(self):
        ''' close the web driver '''
        ltf.write_to_log(
                LOGGER, 
                'INFO', 
                f'Ended: {str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))}\n')
        self.driver.quit()


    def switch_window(self, win_index):
        ''' switch to different tab '''
        self.driver.switch_to.window(self.driver.window_handles[win_index])


    def get_report_data(self):
        try:
            # add to log
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'In get_report_ data method: {str(strftime("%Y-%m-%d_%H:%M:%S", gmtime()))}\n'
            )

            # maximise the screen
            # self.driver.maximize_window()

            self.wdw.until(
                # google AI mode Query: selenium chaining expected conditions
                # result: all_of (AND), any_of (OR), and none_of (NOT) inside 
                # a single WebDriverWait block. These helper functions let you 
                # evaluate multiple states concurrently without writing custom 
                # lambda workarounds.
                EC.all_of(
                    # check for accordion, that loading modal is no longer 
                    # displayed and that the accept necessary cookies only 
                    # button is shown
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#globalAccordionHeader")),
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, "#loading")),
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR, 
                            "#CybotCookiebotDialogBodyButtonDecline"
                        )
                    ),
                )
            )

            # accept necessary cookies which are required
            self.driver.find_element(
                By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonDecline"
            ).click()

            self.wdw.until(
                # wait until the cookie consent banner is no longer showing
                EC.invisibility_of_element_located(
                    (
                        By.CSS_SELECTOR, 
                        "#CybotCookiebotDialogBodyButtonDecline"
                    )
                )
            )

            # add to log and save screen shot
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'Cookie Banner Dismissed: {str(strftime("%H:%M:%S %H:%M:%S", gmtime()))}'
            )
            ss_title = f'1_Cookie_Banner_Dismissed_{str(strftime("%Y%m%d%H%M%S", gmtime()))}'
            self.save_screenshot(ss_title)

            # wait for the search field
            search = self.wdw.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#searchInput'))
            )

            # enter the search paramater
            self.action.move_to_element(search).click().send_keys('TMU M50 001.7N').perform()

            # wait for the search result
            search_result = self.wdw.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mapSearchResults"]/ul/li[1]/span[2]'))
            )
            
            # Add to log and save screen shot
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'Search Result Displayed: {str(strftime("%H:%M:%S %H:%M:%S", gmtime()))}'
            )
            ss_title = f'2_Search_Result_{str(strftime("%Y%m%d%H%M%S", gmtime()))}'
            self.save_screenshot(ss_title)

            # click on the search result to select the data recording station
            self.action.click(search_result).perform()

            # navigate through the accordion
            self.wdw.until(
                EC.all_of(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, '#globalAccordion')),
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '#accordionContent')),
                )
            )

            # get the session ID
            ses_id = self.wdw.until(
                # google search: selenium by xpath partial id
                # result: https://www.tutorialspoint.com/article/how-to-locate-element-by-partial-id-match-in-selenium
                EC.presence_of_element_located(
                    (By.XPATH, '//*[starts-with(@id, "accordion-")]'))
            )

            print(ses_id.get_attribute('id')[10:])

            # create the header class name using the session id
            header = f'sectionHeader{ses_id.get_attribute('id')[10:]}'

            # get accordion elements so that the Reports header can be selected
            accordion_classes = self.driver.find_elements(
                By.CLASS_NAME, header)

            # go through the accordion classes and activate Reports
            for index, div in enumerate(accordion_classes):
                if (div.get_attribute('data-index') == '2') & (div.text == 'Reports'):
                    self.action.pause(1).click(div).perform()


            # wait for the calendar icon to be displayed
            calendar = self.wdw.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'fa-calendar-alt'))
            )

            # Add to log and save screen shot
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'Reports Accordion Section: {str(strftime("%H:%M:%S %H:%M:%S", gmtime()))}'
            )
            ss_title = f'3_Reports_Accordion_{str(strftime("%Y%m%d%H%M%S", gmtime()))}'
            self.save_screenshot(ss_title)

            # click the calendar icon to proceed to the report selection page
            self.action.pause(1).click(calendar).perform()

            # change to the new tab showing the reports page
            self.wdw.until(
                EC.number_of_windows_to_be(2)
            )

            self.driver.switch_to.window(self.driver.window_handles[1])

            # wait for the loading screen to change
            self.wdw.until_not(
                EC.all_of(
                    EC.visibility_of_element_located(
                        (By.ID, 'message')),
                    EC.invisibility_of_element_located(
                        (By.ID, 'top')),
                    EC.invisibility_of_element_located(
                        (By.ID, 'reports')),
                )
            )

            # Add to log and save screen shot
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'Reports Page: {str(strftime("%H:%M:%S %H:%M:%S", gmtime()))}'
            )
            ss_title = f'4_Reports_Page_{str(strftime("%Y%m%d%H%M%S", gmtime()))}'
            self.save_screenshot(ss_title)

            # used to check the class of the element
            self.wdw.until(
                EC.all_of(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="class-tab]')),
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="class-tab]/a'))
                )
            )

            tab = self.driver.find_element(By.XPATH, '//*[@id="class-tab]')
            tab_a = self.driver.find_element(By.XPATH, '//*[@id="class-tab]/a')

            # ensure that the tab is active
            if tab.get_attribute('class') != 'active':
                self.action.pause(1).click(tab_a).perform()

            # Add to log and save screen shot
            ltf.write_to_log(
                LOGGER,
                'INFO',
                f'Report Link: {str(strftime("%H:%M:%S %H:%M:%S", gmtime()))}'
            )
            ss_title = f'5_Report_Link_{str(strftime("%Y%m%d%H%M%S", gmtime()))}'
            self.save_screenshot(ss_title)

            self.driver_quit()
        except:
            print('Exception Raised!')
            self.driver_quit()