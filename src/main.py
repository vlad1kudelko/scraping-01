from selenium.webdriver.common.by import By
import datetime
import json
import pathlib
import re
import time
import undetected_chromedriver as webdriver

#--------------------------------------------------------------------
def parse_page_de(inp_url):
    ret = {}

    driver.get(inp_url)
    driver.reconnect(timeout=10)
    driver.implicitly_wait(5)

    driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-header-rating-action]').click()
    ret['rating'] = driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-info-modal-reviews] div[data-qa=heading]').text
    ret['count'] = driver.find_element(By.CSS_SELECTOR, '[data-qa=restaurant-info-modal-reviews-rating-element] ~ * > *:nth-child(1)').text
    ret['count'] = re.findall(r'\d+', ret['count'].split('\n')[1])[0]
    ret['list'] = []
    print(ret)

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
def parse_page_en(inp_url):
    ret = {}

    wait = 5
    driver.get(inp_url)
    driver.reconnect(timeout=10)
    driver.implicitly_wait(wait)

    ret['count'] = driver.find_element(By.CSS_SELECTOR, '[data-js-test=rating-count-description]').text
    ret['count'] = re.findall(r'\d+', ret['count'])[0]
    driver.find_element(By.CSS_SELECTOR, '[data-js-test=rating-count-description]').click()
    ret['rating'] = driver.find_element(By.CSS_SELECTOR, '.c-reviews-rating [data-test-id=rating-multi-star-component] ~ *').text
    ret['rating'] = re.findall(r'[\d,.]+', ret['rating'])[0]
    ret['list'] = []
    print(ret)

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
        driver.execute_script('document.querySelector(".c-megaModal-document--scrollable").scrollTo(0, 99999999)')
        (lambda x: x[0].click() if len(x) == 1 else '')(driver.find_elements(By.CSS_SELECTOR, '[data-test-id=review-show-more-button]'))
        list_cards = driver.find_elements(By.CSS_SELECTOR, '[data-test-id=review-container]')
        for item_cards in list_cards[len(ret['list']):]:
            driver.implicitly_wait(0.1)
            ret['list'].append({
                'id': '',
                'name': item_cards.find_element(By.CSS_SELECTOR, '[data-test-id=review-author]').text,
                'date': item_cards.find_element(By.CSS_SELECTOR, '[data-test-id=review-date]').text,
                'text': (lambda x: x[0].text if len(x) == 1 else '')(item_cards.find_elements(By.CSS_SELECTOR, '[data-test-id=review-text]')),
            })
            driver.implicitly_wait(wait)
            print('len:', len(ret['list']) )
        time.sleep(1)

    return ret
#--------------------------------------------------------------------
def main():
    list_url = [
        {'url': 'https://www.lieferando.at/speisekarte/vapiano-wien-herrengasse',           'group': 'de'},
        {'url': 'https://www.lieferando.de/speisekarte/peter-pane-hamburg-goldbekplatz',    'group': 'de'},
        {'url': 'https://www.thuisbezorgd.nl/de/speisekarte/vapiano-rembrandtplein',        'group': 'de'},
        {'url': 'https://www.pyszne.pl/menu/vapiano-galeria-mokotow',                       'group': 'de'},
        {'url': 'https://www.just-eat.ch/en/menu/vapiano-zuerich-raemistrasse',             'group': 'de'},

        {'url': 'https://www.just-eat.co.uk/restaurants-vapiano-manchester',                'group': 'en'},
        {'url': 'https://www.just-eat.es/restaurants-vapiano-barcelona',                    'group': 'en'},
        {'url': 'https://www.menulog.com.au/restaurants-vapiano-king-st-sydney',            'group': 'en'},
    ]

    name_dir = pathlib.Path.cwd() / 'out'
    name_file = datetime.datetime.now().isoformat()[:19] + '.jsonl'
    pathlib.Path(name_dir).mkdir(parents=True, exist_ok=True)

    for item_url in list_url:
        if item_url['group'] == 'de':
            ret = parse_page_de(item_url['url'])
        if item_url['group'] == 'en':
            ret = parse_page_en(item_url['url'])
        with open(name_dir / name_file, 'a') as f:
            f.write(json.dumps({
                'input': item_url,
                'output': ret,
            }, ensure_ascii=False) + '\n')
            print('WRITE')
#--------------------------------------------------------------------
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # docker
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    # docker
    driver = webdriver.Chrome(options=options)
    main()
    driver.close()
    driver.quit()
