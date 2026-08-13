from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

from bs4 import BeautifulSoup

import datetime as dt

# https://www.scrapingbee.com/blog/selenium-python/?utm_source=google&utm_medium=cpc&utm_campaign=HD-ScrapingBee-PMax-Global-Prospecting&gad_source=1&gad_campaignid=23542351429&gbraid=0AAAAACSOZONxBwFtfYDJKtzxIrQSlILZE&gclid=CjwKCAjwhNbTBhB4EiwAsFSg-izr-kbI5V3xbs2TriN1-b4lbddFbtEQpPONGY0s1DGlj04o5okcEhoCqwcQAvD_BwE#1-wait-for-elements-with-webdriverwait-and-expected-conditions

try:
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.enable_bidi = True
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Firefox(options=options)
    driver.get("https://trafficdata.tii.ie/")
    action = ActionChains(driver)
    wdw = WebDriverWait(driver, 10)
    wdwl= WebDriverWait(driver, 25)
    home_handle = driver.current_window_handle
    driver.maximize_window()
    # print(home_handle)

    # print('Current URL: ' + driver.current_url)

    wdw.until(
        # google AI mode Query: selenium chaining expected conditions
        # result: all_of (AND), any_of (OR), and none_of (NOT) inside a single 
        # WebDriverWait block. These helper functions let you evaluate multiple 
        # states concurrently without writing custom lambda workarounds.
        EC.all_of(
            # check for accordion, that loading modal is no longer displayed and 
            # and that the accept necessary cookies only button is shown
            EC.presence_of_element_located((By.CSS_SELECTOR, "#globalAccordionHeader")),
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "#loading")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonDecline")),
        )
    )

    # accept necessary cookies which are required
    driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonDecline").click()

    wdw.until(
        # wait until the cookie consent banner is no longer showing
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonDecline"))
    )

    cookies = driver.get_cookies()
    # print(cookies)
    # id = driver.get_cookie('ASPSESSIONIDCADBCSTA')
    # driver.delete_cookie('ASPSESSIONIDCADBCSTA')
    # driver.add_cookie(
    #     {'domain': 'trafficdata.tii.ie', 'httpOnly': False, 'name': 'ASPSESSIONIDCADBCSTA', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': str(id['value'])}
    # )

    search = wdw.until(
        # wait for the search field
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchInput"))
    )

    # enter the required data location
    action.move_to_element(search).click().send_keys("TMU M50 001.7N").perform()

    search_result = wdw.until(
        # wait for the search result
        EC.presence_of_element_located((By.XPATH, '//*[@id="mapSearchResults"]/ul/li[1]/span[2]'))
    )

    # click the search result
    action.click(search_result).perform()

    report = wdw.until(
        EC.all_of(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#globalAccordion')),
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#accordionContent')),
        )
    )

    ses_id = wdw.until(
        # google search: selenium by xpath partial id
        # result: https://www.tutorialspoint.com/article/how-to-locate-element-by-partial-id-match-in-selenium
        EC.presence_of_element_located((By.XPATH, '//*[starts-with(@id, "accordion-")]'))
    )

    # print(ses_id.get_attribute('id')[10:])
    header = 'sectionHeader' + ses_id.get_attribute('id')[10:]

    accordion_classes = driver.find_elements(By.CLASS_NAME, header)

    for index, div in enumerate(accordion_classes):
        # print(index, ': ', div.get_attribute('data-index'))
        if (div.get_attribute('data-index') == '2') & (div.text == 'Reports'):
            # print(div.text)
            action.pause(1).click(div).perform()

    calendar = wdw.until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'fa-calendar-alt'))
    )

    action.pause(1).click(calendar).perform()

    wdw.until(
        EC.number_of_windows_to_be(2)
    )

    # print('Window Handles: ' + str(driver.window_handles))

    driver.switch_to.window(driver.window_handles[1])
    # print('Current URL: ' + driver.current_url)

    wdw.until_not(  # wait for the loading screen to change
        EC.all_of(
            EC.visibility_of_element_located((By.ID, 'message')), 
            EC.invisibility_of_element_located((By.ID, 'top')), 
            EC.invisibility_of_element_located((By.ID, 'reports')),
        )
    )

    wdw.until(  # will be used to check the class of the element
        EC.all_of(
            EC.presence_of_element_located((By.XPATH, '//*[@id="class-tab"]')),
            EC.presence_of_element_located((By.XPATH, '//*[@id="class-tab"]/a')),
        )
    )

    tab = driver.find_element(By.XPATH, '//*[@id="class-tab"]')
    tab_a = driver.find_element(By.XPATH, '//*[@id="class-tab"]/a')

    if tab.get_attribute('class') != 'active':  # ensure that the tab is active
        action.pause(1).click(tab_a).perform()


    report = wdw.until(  # 
        EC.visibility_of_element_located((By.XPATH, '//*[@id="class"]/ul/li[3]/div[2]/a'))
    )

    action.pause(1).click(report).perform()

    wdw.until(
        EC.number_of_windows_to_be(3)
    )

    driver.switch_to.window(driver.window_handles[2])

    new_page = wdw.until(
        EC.all_of(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="top"]')),
            EC.visibility_of_element_located((By.XPATH, '//*[@id="reportTable"]')),
        )            
    )



    # driver.get('https://trafficdata.tii.ie/dsreport.asp?sgid=XzOA8m4lr27P0HaO3_srSB&spid=1ED82FB0D940&reportdate=2026-08-12&enddate=2026-08-12&dimtype=2')

    print('Current URL: ' + driver.current_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print(soup.prettify())

    # try:
    #     wdw.until(
    #         EC.all_of(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="footer"]')),
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="calendar"]')),
    #         )
    #     )
    # except TimeoutException as te:
    #     print(f'Page not loaded!')

    # # print(dt.datetime.now().strftime('%Y-%m-%d%H%M%S%f'))

    # class_tab = wdw.until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'active')),
    # )

    

    # try:
    #     action.move_to_element(class_tab).click().perform()
    # except ElementNotInteractableException as enie:
    #     driver.save_screenshot("ElementNotInteractableException" + dt.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".png")
    # finally:
    #     pass

    # mdcd_report = wdw.until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="71ca167f"]/div[2]/a'))
    # )

    # print(mdcd_report.get_attribute('href'))

    # action.move_to_element(mdcd_report).pause(5).click().perform()

    # wdw.until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="report"]'))
    # )

    driver.save_screenshot("screenshot_" + dt.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".png")
finally:
    driver.quit()
