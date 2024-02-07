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
            info = i.get_attribute("textContent").replace("\n", "").replace("  ", " ")
            if info == "發言日期發言時間公司代號公司名稱主旨":
                info_list.remove(i)
                
        for i in range(0, len(info_list)):
            info = info_list[i]
            
            output = {}
            splited_info = info.text.replace("\n", "").replace("  ", " ").split(" ")
            temp_details = info.find_elements(By.XPATH, ".//input[@type='hidden']")
            details = ""
            for d in temp_details:
                if("1." in d.get_attribute("value")):
                    details = d.get_attribute("value")
                    break

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
            #today_date = "113/02/07"
            if(info["發言日期"] == today_date):
                temp_list.append(info)
        full_output_list = temp_list
        print("今日公告共 %s 筆" % len(full_output_list))
        return full_output_list

    def store_to_mysql(self, host, user, password, database, table, info):
        '''
        將資料存入 MySQL
        '''
        conn = pymysql.connect(host=host, user=user, password=password, database=database, autocommit=True)
        cursor = conn.cursor()
        for i in info:
            
            try:
                script = "insert into %s (info_date, info_time, company_number, company_name, info_title, info_details) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (table, i["發言日期"], i["發言時間"], i["公司代號"], i["公司名稱"], i["主旨"], i["詳細資料"])
                cursor.execute(script)
                print(script)
            except Exception as e:
                print(e)
        
mops_twse_handler = MopsTwseHandler()
info = mops_twse_handler.get_today_info_list()

mops_twse_handler.store_to_mysql(host="127.0.0.1", user="root", password="", database="sys", table="mops_twse", info=info)
        
        