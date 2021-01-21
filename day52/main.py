# Instagram Follower Bot

import time
import random

from selenium import webdriver

import config

# Note: expects Google Chrome and the appropriate ChromeDriver to be properly installed on the system
# https://chromedriver.chromium.org/downloads

# name of the account to get the followers from
SOURCE_ACCOUNT = "chefsteps"
INSTAGRAM_URL = "https://www.instagram.com/"


def instagram_login():
    """Logs in to Instagram."""
    driver.get(url=INSTAGRAM_URL)
    time.sleep(2)

    # accept cookies
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]').click()
    time.sleep(1)

    # enter credentials and submit
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(config.INSTAGRAM_EMAIL)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(config.INSTAGRAM_PASS)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').submit()
    # an "allow notifications" prompt pops up after this, but it can be ignored in this case


def follow_accounts():
    """Attempts to follow, or request to follow, all followers of the defined source Instagram account."""
    driver.get(url=INSTAGRAM_URL + SOURCE_ACCOUNT)
    time.sleep(1)

    # open the followers list
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(1)

    # followers of the source account pop up in a new window
    follower_window = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
    time.sleep(1)
    # for the break condition
    last_follower = None
    while True:
        followers = follower_window.find_elements_by_tag_name("button")
        # check for break condition
        # virtually guaranteed to get blocked from following new accounts long before though
        # unless the source account has like 10 followers... but why use a bot for that?
        if followers[len(followers) - 1] == last_follower:
            break
        # update the last element if the current list
        last_follower = followers[len(followers) - 1]
        for button in followers:
            # follow (or request to) it's an option
            # unfortunately Instagram seems to block you from trying to follow too many at once
            if button.text == "Follow":
                # wait for a variable amount of seconds, to seem more "human" (still gets blocked eventually though)
                time.sleep(random.randrange(3, 10))
                button.click()

        # scroll down and load some more
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', follower_window)
        time.sleep(1)
    # to have some feedback
    # Note: this does not necessarily mean each follower was followed (or requested)
    print("Instagram login failed or bot has reached the end of the followers list.")
    # a little generic perhaps, but it will have to do
    print("Make sure the login credentials have been set up properly or that the bot has not been blocked.")


driver = webdriver.Chrome()

instagram_login()
time.sleep(6)
follow_accounts()

# close the browser window
driver.close()
