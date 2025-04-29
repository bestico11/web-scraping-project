import codecs
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd


class GetFeatures:
    def __init__(self):
        self.driver = None
        self.result_df = None

    def init(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.get_random_user_agent()}')
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # driver.maximize_window()
        time.sleep(5)

    @staticmethod
    def get_random_user_agent():
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Mozilla/5.0 (Linux; Android 10; Pixel 3XL Build/QP1A.191205.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        ]
        return random.choice(user_agents)

    def fill_digikala_side(self):
        self.expand_digikala()
        time.sleep(1)
        self.expand_digikala()
        time.sleep(1)
        a = self.get_value_by_name_digikala('گنجایش کل به فوت')
        b = self.correct_foot_to_liter(self.get_value_by_name_digikala('گنجایش یخچال'))
        c = self.correct_foot_to_liter(self.get_value_by_name_digikala('گنجایش فریزر'))
        d = self.get_value_by_name_digikala('تعداد طبقات یخچال')
        e = self.get_value_by_name_digikala('تعداد طبقات فریزر')
        return (a, b, c, d, e)

    def fill_digikala_dish(self):
        self.expand_digikala()
        time.sleep(1)
        self.expand_digikala()
        time.sleep(1)
        a = self.get_value_by_name_digikala('نمودار میزان مصرف انرژی')
        b = self.get_value_by_name_digikala('میزان صدا')
        c = self.get_value_by_name_digikala('تعداد برنامه های شست‌وشو')
        d = self.get_value_by_name_digikala('ظرفیت (نفر)')
        e = self.get_value_by_name_digikala('متوسط میزان مصرف آب در هر شست و شو')
        return (a, b, c, d, e)

    def fill_digikala_wash(self):
        self.expand_digikala()
        time.sleep(1)
        self.expand_digikala()
        time.sleep(1)
        a = self.get_value_by_name_digikala('نمودار مصرف انرژی')
        a = self.get_value_by_name_digikala('میزان مصرف برق') if a == ' ' else a
        b = self.get_value_by_name_digikala('نوع موتور')
        c = self.get_value_by_name_digikala('تعداد برنامه شستشو')
        d = self.get_value_by_name_digikala('ظرفیت دیگ')
        e = self.get_value_by_name_digikala('سرعت چرخش موتور')
        return (a, b, c, d, e)

    def fill_sallambabaa_side(self):
        a = self.get_value_by_name_sallambabaa('ظرفیت کل یخچال فریزر (فوت)')
        b = self.get_value_by_name_sallambabaa('ظرفیت کل یخچال (لیتر)')
        c = self.get_value_by_name_sallambabaa('ظرفیت کل فریزر (لیتر)')
        d = self.get_value_by_name_sallambabaa('تعداد طبقات یخچال')
        e = self.get_value_by_name_sallambabaa('تعداد طبقات فریزر')
        return (a, b, c, d, e)

    def fill_sallambabaa_dish(self):
        a = self.get_value_by_name_sallambabaa('برچسب مصرف انرژی')
        b = self.get_value_by_name_sallambabaa('صدا')
        c = self.get_value_by_name_sallambabaa('تعداد برنامه های شستشو')
        d = self.get_value_by_name_sallambabaa('ظرفیت شستشو')
        e = self.get_value_by_name_sallambabaa('میزان مصرف آب در هر دور شستشو')
        return (a, b, c, d, e)

    def fill_sallambabaa_wash(self):
        a = self.get_value_by_name_sallambabaa('برچسب مصرف انرژی')
        b = self.get_value_by_name_sallambabaa('نوع موتور')
        c = self.get_value_by_name_sallambabaa('تعداد برنامه های شستشو')
        d = self.get_value_by_name_sallambabaa('ظرفیت لباسشویی')
        e = self.get_value_by_name_sallambabaa('سرعت‌ چرخش')
        return (a, b, c, d, e)

    def fill_torob_side(self):
        self.expand_torob()
        a = self.get_value_by_name_torob("گنجایش", "فوت")
        a = self.get_value_by_name_torob("ظرفیت", "فوت") if a == ' ' else a
        b = self.get_value_by_name_torob("یخچال", "لیتر")
        c = self.get_value_by_name_torob("فریزر", "لیتر")
        d = self.get_value_by_name_torob("طبقات یخچال", "عدد")
        e = self.get_value_by_name_torob("طبقات فریزر", "عدد")
        return (a, b, c, d, e)

    def fill_torob_dish(self):
        self.expand_torob()
        a = self.get_value_by_name_torob("انرژی", "")
        b = self.get_value_by_name_torob("صدا", "")
        c = self.get_value_by_name_torob("برنامه ها", "")
        d = self.get_value_by_name_torob("ظرفیت", "")
        e = self.get_value_by_name_torob("مصرف آب", "")
        return (a, b, c, d, e)

    def fill_torob_wash(self):
        self.expand_torob()
        a = self.get_value_by_name_torob("انرژی", "")
        b = self.get_value_by_name_torob("نوع موتور", "")
        c = self.get_value_by_name_torob("تعداد برنامه", "")
        d = self.get_value_by_name_torob("ظرفیت", "")
        e = self.get_value_by_name_torob("دور موتور", "")
        e = self.get_value_by_name_torob("سرعت", "") if e == ' ' else e
        return (a, b, c, d, e)

    def fill_atramart_side(self):
        a = self.get_value_by_name_atramart("گنجایش کل به فوت")
        b = self.get_value_by_name_atramart("گنجایش یخچال")
        c = self.get_value_by_name_atramart("گنجایش فریز")
        d = self.get_value_by_name_atramart("تعداد طبقات یخچال")
        e = self.get_value_by_name_atramart("تعداد طبقات فریزر")
        return (a, b, c, d, e)

    def fill_atramart_dish(self):
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        return (a, b, c, d, e)

    def fill_atramart_wash(self):
        a = self.get_value_by_name_atramart("مصرف انرژی")
        b = self.get_value_by_name_atramart("نوع موتور")
        c = self.get_value_by_name_atramart("تعداد برنامه شستشو")
        d = self.get_value_by_name_atramart("ظرفیت دیگ")
        e = self.get_value_by_name_atramart("سرعت چرخش موتور")
        return (a, b, c, d, e)

    def fill_entekhabcenter_side(self):
        a = self.get_value_by_name_entekhabcenter('گنجایش کل', 0)
        b = self.get_value_by_name_entekhabcenter('گنجایش یخچال', 0)
        c = self.get_value_by_name_entekhabcenter('گنجایش فریزر', 0)
        d = self.get_value_by_name_entekhabcenter('تعداد طبقات', 0)
        e = self.get_value_by_name_entekhabcenter('تعداد طبقات', 1)
        return (a, b, c, d, e)

    def fill_entekhab_dish(self):
        a = self.get_value_by_name_entekhabcenter('نمودار مصرف انرژی', 0)
        b = self.get_value_by_name_entekhabcenter('میزان صدا', 0)
        c = self.get_value_by_name_entekhabcenter('تعداد برنامه های شستشو', 0)
        d = self.get_value_by_name_entekhabcenter('ظرفیت ظرفشویی', 0)
        e = self.get_value_by_name_entekhabcenter('متوسط میزان مصرف آب در هر شست و شو', 0)
        return (a, b, c, d, e)

    def fill_entekhab_wash(self):
        a = self.get_value_by_name_entekhabcenter('نمودار مصرف انرژی', 0)
        b = self.get_value_by_name_entekhabcenter('نوع موتور', 0)
        c = self.get_value_by_name_entekhabcenter('تعداد برنامه های شستشو', 0)
        d = self.get_value_by_name_entekhabcenter('ظرفیت لباسشویی', 0)
        e = self.get_value_by_name_entekhabcenter('سرعت چرخش موتور', 0)
        return (a, b, c, d, e)

    def get_value_by_name_atramart(self, name):
        next_sibling = ' '
        try:
            element = self.driver.find_element(By.ID, "descbox_container")
            self.driver.execute_script("arguments[0].style.height = '2000px';", element)
            all_divs = self.driver.find_elements(By.TAG_NAME, "div")
            for i in range(len(all_divs) - 1):
                if all_divs[i].text == name:
                    next_sibling = all_divs[i + 2]
                    break
            return self.extract_number(next_sibling.text)
        except Exception as e:
            print("Not Found!")
        return ' '

    def get_value_by_name_entekhabcenter(self, name, i):
        try:
            value_element = self.driver.find_elements(By.XPATH, f"//p[text()='{name}']/following-sibling::p/span")
            txt = self.extract_number(value_element[i].text)
            return ' ' if txt == '' else txt
        except Exception as e:
            print("Not Found!")
        return ' '

    def get_value_by_name_torob(self, name, value):
        try:
            element = self.driver.find_element(By.XPATH,
                                               f"//div[contains(text(), '{name}')]/following-sibling::div[contains(text(), '{value}')]")
            return self.extract_number(element.text)
        except Exception as e:
            print("Not Found!")
        return ' '

    def get_value_by_name_sallambabaa(self, name):
        try:
            element = self.driver.find_element(By.XPATH, f"//dt[contains(text(), '{name}')]/following-sibling::dd[1]")
            return self.extract_number(element.text)
        except Exception as e:
            print("Not Found!")
        return ' '

    def get_value_by_name_digikala(self, name):
        try:
            element = self.driver.find_element(By.XPATH, f"//p[text()='{name}']/following-sibling::div/p")
            return self.extract_number(element.text)
        except Exception as e:
            print("Not Found!")
        return ' '

    def expand_digikala(self):
        try:
            outer_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[span[text()='مشاهده بیشتر']]")))
            outer_span.click()
        except Exception as e:
            try:
                expand_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//span[text()='مشاهده بیشتر']")))
                self.driver.execute_script("arguments[0].click();", expand_element)
            except Exception as e:
                print("Expand Not Found!")

    def expand_torob(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='نمایش تمام مشخصات']")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='نمایش تمام مشخصات']")))
            # driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            print("Expand Not Found!")

    @staticmethod
    def correct_foot_to_liter(txt):
        try:
            if txt < 70:
                return (txt * 28)
        except Exception as e:
            print(txt)
        return txt

    @staticmethod
    def extract_number(text):
        if (text.lower().find('a+++') != -1) | (text.lower().find('+++a') != -1):
            return 1
        if (text.lower().find('a++') != -1) | (text.lower().find('++a') != -1):
            return 2
        if (text.lower() == 'a+') | (text.lower() == '+a'):
            return 3
        if text.lower() == 'a':
            return 4
        if (text.lower() == 'b+') | (text.lower() == '+b'):
            return 5
        if text.lower() == 'b':
            return 6
        if (text.lower() == 'c+') | (text.lower() == '+c'):
            return 7
        if text.lower() == 'c':
            return 8
        if text.lower() == 'd':
            return 9
        if (text.find("دایرکت") != -1) | (text.lower().find("direct") != -1):
            return 1
        if text.find("تسمه") != -1:
            return 2
        # Use regular expression to find the first occurrence of a number in the text
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        else:
            return ' '

    def fill_result_df(self, features, index):
        for i in range(len(features)):
            self.result_df.iloc[index, 6 + i] = features[i] if (
                    (self.result_df.iloc[index, 6 + i] == ' ') & (features[i] != ' ') & (features[i] != None)) else \
                self.result_df.iloc[index, 6 + i]

    def start_feature_extraction(self, repeat=False):
        for i in range(len(self.result_df)):
            if (self.result_df.loc[i, 'link'] == ' ') | ((not self.result_df.loc[i, 'repeat']) & repeat):
                continue
            print('index=', i)
            self.driver.get(self.result_df.loc[i, 'link'])
            time.sleep(random.uniform(5, 8))
            if self.result_df.loc[i, 'category'].find('ساید') != -1:
                if self.result_df.loc[i, 'domain'] == 'digikala.com':
                    features = self.fill_digikala_side()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'sallambabaa.com':
                    features = self.fill_sallambabaa_side()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'torob.com':
                    features = self.fill_torob_side()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'atramart.com':
                    features = self.fill_atramart_side()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'entekhabcenter.com':
                    features = self.fill_entekhabcenter_side()
                    self.fill_result_df(features, i)
            elif self.result_df.loc[i, 'category'].find('ظرفشویی') != -1:
                if self.result_df.loc[i, 'domain'] == 'digikala.com':
                    features = self.fill_digikala_dish()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'sallambabaa.com':
                    features = self.fill_sallambabaa_dish()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'torob.com':
                    features = self.fill_torob_dish()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'atramart.com':
                    features = self.fill_atramart_dish()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'entekhabcenter.com':
                    features = self.fill_entekhab_dish()
                    self.fill_result_df(features, i)
            elif self.result_df.loc[i, 'category'].find('لباسشویی') != -1:
                if self.result_df.loc[i, 'domain'] == 'digikala.com':
                    features = self.fill_digikala_wash()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'sallambabaa.com':
                    features = self.fill_sallambabaa_wash()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'torob.com':
                    features = self.fill_torob_wash()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'atramart.com':
                    features = self.fill_atramart_wash()
                    self.fill_result_df(features, i)
                elif self.result_df.loc[i, 'domain'] == 'entekhabcenter.com':
                    features = self.fill_entekhab_wash()
                    self.fill_result_df(features, i)
            print('features[', f'{i}]=', self.result_df.iloc[i, 6:11])

    def load_file(self, fileName):
        self.result_df = pd.read_csv(fileName, encoding='utf-8')

    def finish(self):
        self.result_df.to_csv('links_and_features.csv', encoding='utf-8', index=False)
        self.driver.quit()
        return 'links_and_features.csv'


if __name__ == '__main__':
    getFeatures = GetFeatures()
    getFeatures.load_file('links_and_features.csv')
    getFeatures.init()
    getFeatures.start_feature_extraction()
    # getFeatures.start_feature_extraction(repeat=True)
    fileName = getFeatures.finish()
