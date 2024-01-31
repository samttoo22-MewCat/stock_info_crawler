import undetected_chromedriver as uc
from auto_download_undetected_chromedriver import download_undetected_chromedriver
import chromedriver_autoinstaller
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from seleniumbase import Driver
from datetime import datetime

class MopsTwseHandler():
    def __init__(self) -> None:
        def get_ChromeOptions(): 
            options = uc.ChromeOptions()
            options.add_argument('--start_maximized')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            #options.add_argument('--headless') 
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            #options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--user-data-dir={}".format(os.path.abspath("profile1")))
            return options
        self.browser_executable_path = ""
        
        print(self.browser_executable_path)
        #download_undetected_chromedriver(self.browser_executable_path, undetected=True, arm=False, force_update=True, dowloadurl=r'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5844.0/win64/chromedriver-win64.zip')
        #chromedriver_autoinstaller.install()
        
        self.browser_executable_path = os.path.abspath("chromedriver.exe")
        #self.driver = uc.Chrome(options=get_ChromeOptions(), version_main=110, use_subprocess=True)
        self.driver = Driver(uc=True)
        
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        
        time_start = datetime.now()
        self.year = eval(time_start.strftime("%Y") + "- 1911")
        self.month = time_start.strftime("%m")
        self.day = time_start.strftime("%d")
        print(self.year, self.month, self.day)
        
        self.driver.get("https://mops.twse.com.tw/mops/web/t05st02")
    
    def get_today_info(self):
        year_input = self.driver.find_element(By.XPATH, "//input[@id='year']")
        year_input.send_keys(self.year)
        
        month_select = Select(self.driver.find_element(By.XPATH, "//select[@id='month']"))
        month_select.select_by_value(self.month)
        
        day_select = Select(self.driver.find_element(By.XPATH, "//select[@id='day']"))
        day_select.select_by_value(self.day)
        
        search_button = self.driver.find_element(By.XPATH, "//div[@id='search_bar1']/div/input[@value=' 查詢 ']")
        self.wait.until(EC.element_to_be_clickable(search_button))
        search_button.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//th[text()='發言日期']")))
        info_list = self.driver.find_elements(By.XPATH, "//div[@id='table01']/table[3]/tbody/tr")
        for i in info_list:
            print(i.text)

mops_twse_handler = MopsTwseHandler()
mops_twse_handler.get_today_info()
        
        