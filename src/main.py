from selenium.webdriver.common.by import By
import re
import time
import undetected_chromedriver as webdriver

#--------------------------------------------------------------------
def parse_page(inp_url):
    ret = {}

    driver.get(inp_url)
    driver.reconnect(timeout=8)
    driver.implicitly_wait(5)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-header-rating-action]').click()
    ret['rating'] = driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-info-modal-reviews] div[data-qa=heading]').text
    ret['count'] = driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-info-modal-reviews-rating-element] ~ * > *:nth-child(1)').text
    ret['count'] = re.findall(r'\d+', ret['count'].split('\n')[1])[0]
    ret['list'] = []

    gameover= {'old_count': 0, 'count_iter': 0}
    while len(ret['list']) != ret['count']:
        # gameover
        if gameover['old_count'] == len(ret['list']):
            gameover['count_iter'] += 1
            print('strike', gameover)
        else:
            gameover['count_iter'] = 0
        if gameover['count_iter'] == 5:
            break
        gameover['old_count'] = len(ret['list'])
        # gameover
        driver.execute_script('document.querySelector("[data-qa=modal-scroll-content]").scrollTo(0, 99999999)')
        list_cards = driver.find_elements(By.CSS_SELECTOR, '[data-qa=review-card-component-element]')
        for item_cards in list_cards:
            current_id = item_cards.find_element(By.CSS_SELECTOR, '[id^=label]').get_attribute('id').split('-')[1]
            if current_id not in [ i['id'] for i in ret['list'] ]:
                ret['list'].append({
                    'id': current_id,
                    'name': item_cards.find_element(By.CSS_SELECTOR, '[id^=label] > *:nth-child(1) > *:nth-child(1)').text,
                    'date': item_cards.find_element(By.CSS_SELECTOR, '[id^=label] > *:nth-child(1) > *:nth-child(2)').text,
                })
                print('len:', len(ret['list']) )
        time.sleep(1)

    return ret
#--------------------------------------------------------------------
def main():
    #  url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
    url = 'https://www.lieferando.at/speisekarte/vapiano-wien-herrengasse'
    #  url = 'https://nowsecure.nl/'

    print(parse_page(url))
#--------------------------------------------------------------------
if __name__ == '__main__':
    driver = webdriver.Chrome()
    main()

#  try:
    #  pass
#  except Exception as ex:
    #  print(ex)
#  finally:
    #  driver.close()
    #  driver.quit()
