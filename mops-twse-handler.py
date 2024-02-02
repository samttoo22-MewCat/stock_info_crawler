import json
import os
import pymysql
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
        
        self.browser_executable_path = os.path.abspath("chromedriver.exe")
        self.driver = Driver(uc=True)
        
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        
        time_start = datetime.now()
        self.year = eval(time_start.strftime("%Y") + "- 1911")
        self.month = time_start.strftime("%m")
        self.day = time_start.strftime("%d")
        
        self.driver.get("https://mops.twse.com.tw/mops/web/t05st02")
    
    def get_today_info_list(self):
        '''
        抓取本日於 https://mops.twse.com.tw/mops/web/t05st02 上公告的資訊，並以列表形式回傳。
        '''
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
        full_output_list = []
        
        for i in info_list:
            if i.text == "發言日期 發言時間 公司代號 公司名稱 主旨":
                info_list.remove(i)
                
        for i in range(0, len(info_list)):
            info = info_list[i]
            def get_details():
                more_info_button = info.find_elements(By.XPATH, "./td/form/input[@type='hidden']")
                more_info_button = more_info_button[len(more_info_button) - 1]
                return more_info_button.get_attribute("value")
            output = {}
            splited_info = info.text.replace("\n", "").replace("  ", " ").split(" ")
            details = get_details()

            output.update({"發言日期": splited_info[1]})
            output.update({"發言時間": splited_info[2]})
            output.update({"公司代號": splited_info[3]})
            output.update({"公司名稱": splited_info[4]})
            output.update({"主旨": splited_info[5]})
            output.update({"詳細資料": details})
            full_output_list.append(output)
            
        temp_list = []
        for i in range(0, len(full_output_list)):
            info = full_output_list[i]
            today_date = "%s/%s/%s" % (self.year, self.month, self.day)
            if(info["發言日期"] == today_date):
                temp_list.append(info)
        full_output_list = temp_list
        
        return full_output_list

    def store_to_mysql(self, host, user, password, database, table, info):
        '''
        將資料存入 MySQL
        '''
        info = self.get_today_info_list()
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute("")
        conn.commit()
mops_twse_handler = MopsTwseHandler()
mops_twse_handler.store_to_mysql()
        
        