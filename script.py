from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium_stealth import stealth

from os import getcwd
from time import sleep
from random import choice


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/106.0.0.0 Safari/537.36')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(getcwd() + '/chromedriver')

    driver = webdriver.Chrome(options=options, service=service)

    stealth(
        driver=driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver


def vk_auth(browser, login, password):
    browser.get('https://vk.com/')

    browser \
        .find_element(By.XPATH, '//*[@id="index_email"]') \
        .send_keys(login)

    browser \
        .find_element(By.XPATH, '//*[@id="index_login"]/div/form/button[1]/span') \
        .click()

    sleep(2)

    browser \
        .find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div'
                                '/div/form/div[1]/div[3]/div[1]/div/input') \
        .send_keys(password)

    browser \
        .find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div'
                                '/div/div/form/div[2]/button') \
        .click()

    sleep(3)

    return browser


def mos_auth(browser, login, password):
    browser.get('https://ag.mos.ru/home')

    # Auth in mos.ru
    browser \
        .find_element(By.XPATH, '/html/body/app-root/ag-page-with-sidebar-layout'
                                '/ag-header/header/ag-auth-actions/button[1]/span') \
        .click()

    browser \
        .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/div/ag-auth-modal'
                                '/ag-modal-container/ag-auth-form/div[1]/button/span/span') \
        .click()

    sleep(2)

    browser \
        .find_element(By.XPATH, '//*[@id="login"]') \
        .send_keys(login)

    browser \
        .find_element(By.XPATH, '//*[@id="password"]') \
        .send_keys(password)

    browser \
        .find_element(By.XPATH, '//*[@id="bind"]') \
        .click()

    # Modal closing if exist
    try:
        browser \
            .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/button') \
            .click()
    except exceptions.NoSuchElementException:
        pass

    return browser


def vk_repost(browser):
    browser \
        .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/div'
                                '/ag-modal-social-fill-success'
                                '/ag-modal-container/div[2]/div/button[1]') \
        .click()

    sleep(2)

    browser \
        .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/div'
                                '/ag-modal-social-share/ag-modal-container'
                                '/div[2]/ul/li[1]/button') \
        .click()

    browser.switch_to.window(browser.window_handles[1])

    sleep(2)

    browser \
        .find_element(By.XPATH, '//*[@id="post_button"]') \
        .click()

    browser.switch_to.window(browser.window_handles[0])

    return browser


def vote_scenario(browser, mos_login, mos_password, vk_login, vk_password):
    vk_auth(browser, vk_login, vk_password)

    mos_auth(browser, mos_login, mos_password)

    # Votes list opening
    browser \
        .find_element(By.XPATH, '/html/body/app-root/ag-page-with-sidebar-layout'
                                '/ag-header/header/div/ag-header-nav/nav'
                                '/ag-list-with-more-button/nav/ul/li[1]/a/span')\
        .click()

    sleep(2)

    browser \
        .find_element(By.XPATH, '/html/body/app-root/ag-page-with-sidebar-layout'
                                '/main/ag-page-layout/ag-sidebar-wrapper/section[1]'
                                '/ag-poll-list/section/ag-list-filter-by-type/div/div/div/a[2]')\
        .click()

    # Voting cycle
    while True:
        try:
            browser \
                .find_element(By.XPATH, '/html/body/app-root/ag-page-with-sidebar-layout'
                                        '/main/ag-page-layout/ag-sidebar-wrapper/section[1]'
                                        '/ag-poll-list/section/ag-poll-cards-set/ag-cards-grid'
                                        '/ag-poll-card[1]')\
                .click()
        except exceptions.NoSuchElementException:
            break

        sleep(2)

        for poll in browser.find_elements(By.TAG_NAME, 'ag-poll-question'):
            poll \
                .find_element(By.TAG_NAME, 'ag-variant')\
                .click()

        try:
            browser.find_element(By.TAG_NAME, 'ag-modal')

            browser \
                .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/div'
                                        '/ag-modal-input-text/ag-modal-container'
                                        '/form/textarea')\
                .send_keys(choice('!@#$%^&*()_-+='))

            browser \
                .find_element(By.XPATH, '/html/body/ag-modal/div[2]/div/div'
                                        '/ag-modal-input-text/ag-modal-container'
                                        '/div/button[2]')\
                .click()
        except exceptions.NoSuchElementException:
            pass

        browser \
            .find_element(By.XPATH, '/html/body/app-root/ag-page-with-sidebar-layout'
                                    '/main/ag-page-layout/ag-sidebar-wrapper/section[1]'
                                    '/ag-poll-page/ag-poll/div/button')\
            .click()

        sleep(2)

        vk_repost(browser)

        browser.back()
        browser.refresh()

        sleep(2)


if __name__ == '__main__':
    vote_scenario(
        browser=create_driver(),
        mos_login='',
        mos_password='',
        vk_login='',
        vk_password=''
    )
