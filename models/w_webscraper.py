# packages - selenium, webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import re
import time

# things to do before launch -> increase wait time limit

def w_scrape():
    # store_info = []
    vegetable_info = []

    # adding customizations
    options = Options()

    ## running chrome headless(invisble mode)
    # options.add_argument("--headless")

    # customizing window size
    options.add_argument("--window-size=1920,1200")

    # passing chrome driver as service
    service = Service(ChromeDriverManager().install())

    # initiating driver
    driver = webdriver.Chrome(service=service, options=options)

    # # jumping directly into vegetable section
    driver.get("https://www.woolworths.com.au/shop/browse/fruit-veg/vegetables")

    wait = WebDriverWait(driver, 25)

    # closing popups if there is any
    # create an instance of ActionChains
    actions = ActionChains(driver)
    actions.move_by_offset(1, 1).click().perform()
    time.sleep(1)
    actions.move_by_offset(1, 1).click().perform()
    time.sleep(3)

    # extract data from each page
    while True:

        time.sleep(10)

        # accesing all grids
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search-content"]/div/shared-grid/div/div')))
        div_elements = driver.find_elements(By.XPATH, '//*[@id="search-content"]/div/shared-grid/div/div')

        for each_veg in div_elements:
            # cart condition element
            cart = each_veg.find_elements(By.XPATH, './/button[1]/span[@class="cartControls-addCart"]')

            if cart and cart[0].text.lower().strip() == 'add to cart':
                all_info = (each_veg.text.lower().split('\n'))[1:3]

                # extracting price and checking price condition
                if not re.search(r'1?kg$', all_info[0]):
                    continue

                # extracting name -removing 'woolworths' 'xxxg' from name
                veg_price = (re.search(r'\d{1,3}.\d{2}', all_info[0])).group()
                veg_name = all_info[1].lower().replace('woolworths', '').strip()
                temp = re.search(r'\s\d{3}g', veg_name)
                if temp:
                    veg_name = veg_name.replace(temp.group(), "")

                # saving extracted indvd veg info
                if veg_name and veg_price:
                    vegetable_info.append({veg_name: veg_price})

        # locate the button element
        button = driver.find_elements(By.XPATH, '//*[@id="search-content"]//div/div[@class="paging-section"]/a[@rel="next"]')
        # check if the button is enabled
        if button:
            if button[0].is_enabled():
                button[0].click()
        else:
            return vegetable_info

# # delete this
# print(w_scrape())


