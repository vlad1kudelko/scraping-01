from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#  from selenium.webdriver.common.by import By
import os
import time

#  url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
url = 'https://nowsecure.nl'

s = Service()
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=s, options=options)

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    '''
})

driver.maximize_window()
driver.get(url)
time.sleep(60)


#  ############### Cloudflare bypass ###############
#  # adspower.com/ru/blog/bypass-cloudflare-detection-with-selenium
#  handle = driver.current_window_handle
#  driver.service.stop()
#  time.sleep(6)
#  driver = webdriver.Chrome(options=options)
#  driver.switch_to.window(handle)
#  ############### Cloudflare bypass ###############
