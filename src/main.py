from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as webdriver

#--------------------------------------------------------------------
def main():
    #  url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
    url = 'https://www.lieferando.at/speisekarte/vapiano-wien-herrengasse'
    #  url = 'https://nowsecure.nl/'

    driver = webdriver.Chrome()

    driver.get(url)
    driver.reconnect(timeout=6)

    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '*[data-qa="restaurant-header-rating-action"]').click()
    driver.find_element(By.CSS_SELECTOR, '*[data-qa=restaurant-info-modal-reviews] div[data-qa=heading]').text

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
