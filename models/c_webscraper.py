from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import re
import time

def c_scrape():
    # before launch -> increase wait time

    # can be either pin or place name , "sydney"
    scraper_for_address = ["wollongong", "fairy meadow"]

    output = []

    for each_place in scraper_for_address:

        store_info = []
        vegetable_info = []

        # adding customizations
        options = Options()

        # running chrome headless(invisble mode)
        options.add_argument("--headless")

        # customizing window size
        options.add_argument("--window-size=1920,1200")

        # passing chrome driver as service
        service = Service(ChromeDriverManager().install())

        # initiating driver
        driver = webdriver.Chrome(service=service, options=options)

        # # jumping directly into vegetable section
        driver.get("https://www.coles.com.au/browse/fruit-vegetables/vegetables")

        wait = WebDriverWait(driver, 25)

        # closing popups if there is any
        # create an instance of ActionChains
        actions = ActionChains(driver)
        actions.move_by_offset(1, 1).click().perform()
        time.sleep(1)
        actions.move_by_offset(1, 1).click().perform()
        time.sleep(3)

        # clicking - set shopping method
        wait.until(EC.visibility_of_element_located((By.ID, "delivery-selector-button")))
        driver.find_element(By.ID, "delivery-selector-button").click()

        time.sleep(3)

        # selecting and entering postcode
        xpath = "//div[@id='shopping-method-tab-0']//input[@type='text']"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(each_place)

        time.sleep(3)

        # press enter
        xpath = '//*[@id="shopping-method-tab-0"]/div[1]/div/div[2]/div/div/div'
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.send_keys(Keys.ENTER)

        time.sleep(3)

        # # no result case
        # xpath = '//*[@id="shopping-method-tab-0"]//*[@role="listbox"]/*[1]'
        # wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        # element = driver.find_element(By.XPATH, xpath)
        # text = element.text.lower()
        # if text == "no results found":
        #     print("nothing found")
        #     continue

        time.sleep(3)

        # finding options list
        xpath = "//div[@role='tabpanel'][@id='shopping-method-tab-0']//*[@role='radiogroup']/div/div[position()<6]"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        inner_divs = driver.find_elements(By.XPATH, xpath)

        time.sleep(3)

        # checking which store fits
        for div in inner_divs:
            store_name = div.find_element(By.XPATH, "./label/span/span/span[1]")
            if "coles" not in store_name.text.lower():
                print("text do not contain coles")
                continue
            store_info.append(store_name.text.lower())
            store_addr = div.find_element(By.XPATH, "./label/span/span/address[position()=1]")
            store_info.append(store_addr.text.lower())

            # clicking the store_name
            store_name.click()

            # clicking set location
            xpath = '//div[@id="shopping-method-tab-0"]/div[3]/button[1]'
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            driver.find_element(By.XPATH, xpath).click()
            break

        time.sleep(3)

        # extracting data from each page
        while True:

            time.sleep(7)

            wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="coles-targeting-product-tiles"]/section')))
            all_sections = driver.find_elements(By.XPATH, '//*[@id="coles-targeting-product-tiles"]/section')

            for each_veg in all_sections:
                temp = None
                try:
                    temp = each_veg.find_element(By.XPATH, './/div[3]/div[@aria-hidden="false"]/section/span[2]')
                except NoSuchElementException:
                    continue

                if temp is not None:
                    # name extraction
                    veg_name = each_veg.find_element(By.XPATH, './/h2').text
                    veg_name = veg_name.lower().replace('coles', '').split("|")[0].strip()

                    # price extraction
                    veg_price = each_veg.find_element(By.XPATH,
                                                      './/div[@class="product__cta_section"]//span[@class="price__calculation_method"]')

                    # re it
                    veg_price = veg_price.text
                    veg_match = re.search(r'\.*\d{1,3}.\d{1,3}\.*', veg_price)

                    # move to next iteration if veg_name is empty
                    if not veg_match:
                        continue
                    veg_price = veg_match.group()

                    # adding extracted info to output
                    veg_appender = {veg_name: veg_price}
                    vegetable_info.append(veg_appender)

            # locate the button element
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="pagination-button-next"][@aria-label="Go to next page"]')))
            button = driver.find_element(By.XPATH, '//*[@id="pagination-button-next"][@aria-label="Go to next page"]')

            # check if the button is enabled
            if button.is_enabled():
                button.click()
            else:
                break

        # adding data to output
        if store_info and vegetable_info:
            output.append([store_info,vegetable_info])

        driver.quit()

    return output


# # delete this
# text_list = c_scrape()
# for each in text_list:
#     print(each)
