import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pyquery import PyQuery as  pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)
action = ActionChains(browser)
browser.set_window_size(1400, 900)

def search():
    print('正在搜索')
    try:
        browser.get('http://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
            # EC.presence_of_element_located((By.ID, "q"))      ID
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  # clickable是按钮可点击方法
        input.send_keys(KEYWORD)
        submit.click()
        login = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fm-login-id"))
        )
        login.send_keys(username)
        passwd = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fm-login-password"))
        )
        passwd.send_keys(password)
        loging = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#login-form > div.fm-btn > button")
        ))
        loging.click()
        dragger = browser.find_element_by_id('nc_1_n1z')
        action.drag_and_drop_by_offset(dragger, 258, 258).perform()
        sleep(2)
        loging.click()
        page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_products()
        return page.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在翻页')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
            # EC.presence_of_element_located((By.ID, "q"))      ID
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))  # clickable是按钮可点击方法
        input.clear()
        input.send_keys(page_number)
        submit.click()  # 点击submit标签
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            '图片': item.find('.pic .img').attr('src'),
            '价格': item.find('.price').text(),
            '销量': item.find('.deal-cnt').text(),
            '商品名称': item.find('.title').text(),
            '店铺名称': item.find('.shop').text(),
            '地址': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("保存MongoDB成功", result)
    except Exception:
        print('存储到MongoDB错误', result)


def main():

        page = search()
        page = int(re.compile('(\d+)').search(page).group(1))
        for i in range(2, page + 1):
            next_page(i)

        browser.close()


if __name__ == '__main__':
    main()
