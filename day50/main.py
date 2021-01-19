# Auto Tinder Swiper

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import config

# Note: expects Google Chrome and the appropriate ChromeDriver to be properly installed on the system
# https://chromedriver.chromium.org/downloads

FACEBOOK_URL = "https://www.facebook.com/"
TINDER_URL = "https://tinder.com/"
# there's a daily limit for swipes, apparently
DAILY_LIMIT = 100


def facebook_login():
    """Logs in to Facebook."""
    driver.get(url=FACEBOOK_URL)
    time.sleep(2)
    # accept all cookies
    driver.find_element_by_id("u_0_h").click()
    # enter credentials and submit
    driver.find_element_by_id("email").send_keys(config.FACEBOOK_EMAIL)
    driver.find_element_by_id("pass").send_keys(config.FACEBOOK_PASS)
    driver.find_element_by_id("pass").submit()


def tinder_login():
    """Logs in to Tinder using Facebook."""
    driver.get(url=TINDER_URL)
    time.sleep(2)
    # accept privacy notice
    driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button').click()
    time.sleep(1)
    # click on login button
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div/'
                                 'header/div/div[2]/div[2]/button').click()
    time.sleep(1)
    # click on facebook button
    driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button').click()
    time.sleep(1)

    # accept to associate with Facebook account... this is just a one-time permission
    try:
        driver.find_element_by_xpath('//*[@id="u_0_4"]/div[2]/div[2]/div[1]/button').click()
    except NoSuchElementException:
        # no need to do anything
        pass
    time.sleep(2)

    # allow location
    driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
    time.sleep(2)
    # disallow notifications
    driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]').click()
    time.sleep(2)

    # in case it pops up, on "see who likes you", click "maybe later"
    try:
        driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div[3]/button[2]').click()
    except NoSuchElementException:
        # no need to do anything here either
        pass


def swipe(swipe_right=False):
    """Swipes left unless "swipe_right=True" is specified."""
    # using the key controls to make things simpler
    nav = driver.find_element_by_id("Tinder")
    if swipe_right:
        nav.send_keys(Keys.RIGHT)
        time.sleep(1)
        # in case there is a match, close the pop-up
        # Note: there might be other pop-ups when sweeping right, but testing it was kept to the bare minimum
        try:
            driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button').click()
        except NoSuchElementException:
            pass
        else:
            time.sleep(1)
    else:
        nav.send_keys(Keys.LEFT)


driver = webdriver.Chrome()
# log in to Facebook, make sure the credentials were set properly
facebook_login()
time.sleep(5)
# log in to Tinder
tinder_login()
time.sleep(2)

# keep swiping until the limit
for _ in range(DAILY_LIMIT):
    # it will swipe left unless explicitly specified to swipe right with "swipe_right=True"
    swipe()
    time.sleep(1)

# close the browser window
driver.close()
