from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver

#--------------------------------------------------------------------
def main():
    #  url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
    url = 'https://www.lieferando.at/speisekarte/vapiano-wien-herrengasse'
    #  url = 'https://www.lieferando.de/'
    #  url = 'https://nowsecure.nl/'

    driver = undetected_chromedriver.Chrome()
    driver.get(url)

    ############### Cloudflare bypass ###############
    # adspower.com/ru/blog/bypass-cloudflare-detection-with-selenium
    handle = driver.current_window_handle
    driver.service.stop()
    time.sleep(6)
    driver = undetected_chromedriver.Chrome()
    driver.switch_to.window(handle)
    ############### Cloudflare bypass ###############
    print('good')

    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '*[data-qa="restaurant-header-rating-action"]').click()

    time.sleep(9999)
#--------------------------------------------------------------------
if __name__ == '__main__':
    main()

#  try:
    #  pass
#  except Exception as ex:
    #  print(ex)
#  finally:
    #  driver.close()
    #  driver.quit()
