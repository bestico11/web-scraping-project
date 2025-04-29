import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd


class GetLinks:
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

    def search(self, model, domain='digikala.com', engine='yahoo.com'):
        self.driver.get(self.get_engine_query_by(model, domain, engine))
        time.sleep(random.uniform(14, 18))
        first_link = ' '
        first_result = ''
        try:
            first_result = self.driver.find_element(By.XPATH, self.get_engine_link_by(engine))
            first_link = first_result.get_attribute("href")
        except Exception as e:
            try:
                first_result = self.driver.find_element(By.XPATH, self.get_alternative_engine_link_by(engine))
                first_link = first_result.get_attribute("href")
            except Exception as e:
                print("Link Not Found!")
        finally:
            print('link: ', first_link)
        text = ' '
        try:
            text = first_result.text
        except Exception as e:
            print('text = ', text, '!')
        #driver.quit()
        if self.check_link_authenticity(engine, domain, model, first_link, text):
            return first_link
        return ' '

    @staticmethod
    def get_engine_query_by(model, domain, engine):
        match engine:
            case 'google.com':
                return 'https://www.google.com/search?q=' + model + '++site%3A+' + domain + '&sca_esv=9a8b494ebc885c97&rlz=1C1GGRV_enIR1143IR1143&sxsrf=AHTn8zp0LxYiq4f6CB2Jxwv9hantqrl4cQ%3A1740218130724&ei=Ep-5Z9TwK4iM9u8PoOnSUA&ved=0ahUKEwjUwY3cgdeLAxUIhv0HHaC0FAoQ4dUDCBA&uact=5&oq=DAEWOO-SBS-DS-3020MW++site%3Adigikala.com&gs_lp=Egxnd3Mtd2l6LXNlcnAiJ0RBRVdPTy1TQlMtRFMtMzAyME1XICBzaXRlOmRpZ2lrYWxhLmNvbUioW1AVWKNXcAF4AZABAJgBnQSgAecHqgEFNC0xLjG4AQPIAQD4AQH4AQKYAgKgAq0EwgIKEAAYsAMY1gQYR8ICBRAAGO8FmAMAiAYBkAYIkgcFMS40LTGgB5kE&sclient=gws-wiz-serp'
            case 'yahoo.com':
                return 'https://search.yahoo.com/search?p=' + model + '+site%3A+' + domain + '&fr=yfp-t&fr2=p%3Afp%2Cm%3Asb&ei=UTF-8&fp=1'
            case 'bing.com':
                return 'https://www.bing.com/search?q=' + model + '+site%3A+' + domain + '&form=QBLH&sp=-1&lq=0&pq=daewoo-sbs-ds-3320mw+site%3A+digikala.com&sc=0-39&qs=n&sk=&cvid=9F7D0B8218834BFD9169892E6F8593C8&ghsh=0&ghacc=0&ghpl='
            case 'yandex.com':
                return 'https://yandex.com/search/?text=' + model + '+site%3A+' + domain + '&lr=112699&family=yes'
            case _:
                return ' '

    @staticmethod
    def get_engine_link_by(engine):
        match engine:
            case 'google.com':
                return '(//a/h3)[1]/..'
            case 'yahoo.com':
                return '//h3/a[1]'
            case 'bing.com':
                return '//h2/a[1]'
            case 'yandex.com':
                return '//h2[1]/ancestor::a[1]'
            case _:
                return ' '

    @staticmethod
    def get_alternative_engine_link_by(engine):
        match engine:
            case 'google.com':
                return '(//a/h3)[2]/..'
            case 'yahoo.com':
                return '//h3/a[2]'
            case 'bing.com':
                print('alt ')
                return '//h2[1]/ancestor::a[1]'
            case 'yandex.com':
                return '//h2[2]/ancestor::a[1]'
            case _:
                return ' '

    @staticmethod
    def calculate_similarity(similarity, model, link):
        start_index = 0
        link = link.lower().replace('-', '').replace('/', '').replace('%', '').replace(' ', '')
        model = model.lower().replace('-', '')[-9:]
        for i, m in enumerate(model):
            for j, l in enumerate(link):
                if m == l:
                    if (link[j:j + similarity] == model[i:i + similarity]) & (
                            len(link[j:j + similarity]) == similarity):
                        print('sim= ', model[i:i + similarity], '!')
                        return True
        return False

    def check_link_authenticity(self, engine, domain, model, first_link, text):
        if (first_link.lower().find(engine.lower()) != -1) & (self.calculate_similarity(4, model, text)):
            print("It's OK")
            return True
        if first_link.lower().find(domain.lower()) == -1:
            return False
        if self.calculate_similarity(5, model, first_link):
            print("It's OK")
            return True
        if (first_link.lower().find(domain.lower()) != -1) & self.calculate_similarity(4, model, text):
            print("It's OK")
            return True
        return False

    @staticmethod
    def get_random_engine():
        return random.choice(['yahoo.com', 'bing.com'])

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

    def fill_the_link_for(self, i, model, domain, engine):
        self.result_df.loc[i, 'link'] = self.search(model, domain, engine)
        time.sleep(random.uniform(1, 5))
        if self.result_df['link'][i] != ' ':
            self.result_df.loc[i, 'domain'] = domain
            self.result_df.loc[i, 'engine'] = engine
            return True
        return False

    @staticmethod
    def is_empty(features):
        count = 0
        for i in range(len(features)):
            count = (count + 1) if ((features.iloc[i] == ' ') | (features.iloc[i] == None)) else count
        if count >= 2:
            return True
        return False

    def start_link_engine(self, domainList, repeat=False):
        for i, model in enumerate(self.result_df['model']):
            if (self.result_df['link'][i] == ' ') | (repeat & self.is_empty(self.result_df.iloc[i, 6:11])):
                print('index= ', i)
                model = self.result_df['category'][i] + ' ' + model
                flag = self.fill_the_link_for(i, model, domainList[0], 'yahoo.com')
                if not flag:
                    flag = self.fill_the_link_for(i, model, domainList[1], 'bing.com')
                    if not flag:
                        flag = self.fill_the_link_for(i, model, domainList[2], self.get_random_engine())
                        if not flag:
                            flag = self.fill_the_link_for(i, model, domainList[3], 'yahoo.com')
                            if not flag:
                                flag = self.fill_the_link_for(i, model, domainList[4], 'bing.com')
                self.result_df.loc[i, 'repeat'] = flag if repeat else False


    def first_init_load_file(self, fileName):
        file = pd.read_excel(fileName)
        df = pd.DataFrame(file.iloc[:, 0:3])
        df.columns = ['category', 'brand', 'model']
        self.result_df = df.groupby(['category', 'brand']).apply(lambda x: x.head(2)).reset_index(drop=True)
        self.result_df['link'] = ' '
        self.result_df['engine'] = ' '
        self.result_df['domain'] = ' '
        self.result_df['att1'] = ' '
        self.result_df['att2'] = ' '
        self.result_df['att3'] = ' '
        self.result_df['att4'] = ' '
        self.result_df['att5'] = ' '
        self.result_df['repeat'] = False

    def load_file(self, fileName):
        self.result_df = pd.read_csv(fileName, encoding='utf-8')

    def finish(self):
        self.result_df.to_csv('links_and_features.csv', encoding='utf-8', index=False)
        self.driver.quit()
        return 'links_and_features.csv'


if __name__ == '__main__':
    getLink = GetLinks()
    getLink.first_init_load_file('code.xlsx')
    getLink.init()
    domainList1 = ['digikala.com', 'sallambabaa.com', 'torob.com', 'atramart.com', 'entekhabcenter.com']
    getLink.start_link_engine(domainList1)
    # domainList2 = ['entekhabcenter.com', 'atramart.com', 'torob.com', 'sallambabaa.com', 'digikala.com']
    # getLink.start_link_engine(domainList2, repeat=True)
    fileName = getLink.finish()
