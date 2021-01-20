# Internet Speed Twitter Bot

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import config

# Note: expects Google Chrome and the appropriate ChromeDriver to be properly installed on the system
# https://chromedriver.chromium.org/downloads

# change to "@Comcast" or whatever the company's Twitter handle is
ISP_NAME = "Internet Provider"
# "guaranteed" internet speeds in Mbps
MIN_DOWNLOAD_SPEED = 300
MIN_UPLOAD_SPEED = 30
SPEEDTEST_URL = "https://www.speedtest.net/"
TWITTER_LOGIN_URL = "https://twitter.com/login/"


def test_speed():
    """Checks the internet connection and returns the results as a TUPLE."""
    driver.get(url=SPEEDTEST_URL)
    time.sleep(2)

    # consent to cookies
    driver.find_element_by_id("_evidon-banner-acceptbutton").click()
    time.sleep(2)

    # start the test
    driver.find_element_by_class_name("js-start-test").click()
    # the test seems to take around 40 seconds, doubling that to be safe
    time.sleep(80)

    # close the Speedtest for Windows ad
    # assuming that on different systems a different variant might pop up, or none at all
    try:
        driver.find_element_by_link_text("Back to test results").click()
    except NoSuchElementException:
        pass
    time.sleep(2)

    # get the results
    # ping-speed
    ping_speed = driver.find_element_by_class_name("ping-speed").text
    # download-speed
    dl_speed = driver.find_element_by_class_name("download-speed").text
    # upload-speed
    ul_speed = driver.find_element_by_class_name("upload-speed").text

    # also return the current url, it's the link to the results
    return ping_speed, dl_speed, ul_speed, driver.current_url


def twitter_login():
    """Logs in to Twitter."""
    driver.get(url=TWITTER_LOGIN_URL)
    time.sleep(2)
    driver.find_element_by_name("session[username_or_email]").send_keys(config.TWITTER_EMAIL)
    driver.find_element_by_name("session[password]").send_keys(config.TWITTER_PASS)
    driver.find_element_by_name("session[password]").submit()
    # Note: at one of the attempts, there was some data sharing notice that needed to be accepted
    # however, it wasn't possible to reproduce it, even using multiple accounts


def send_tweet(ping_speed, dl_speed, ul_speed, url):
    """Takes internet speed details and tweets them at the defined name."""
    twitter_login()
    time.sleep(2)
    # to make sure the user has really logged in
    try:
        entry_field = driver.find_element_by_class_name("public-DraftStyleDefault-block")
    except NoSuchElementException:
        print("It was not possible to send a tweet. Make sure the Twitter credentials have been set up properly.")
    else:
        time.sleep(2)
        # format the message
        message = f"Hey {ISP_NAME}, why is my ping {ping_speed}ms and internet speed {dl_speed}Mbps down & " \
                  f"{ul_speed}Mbps up when I pay for {MIN_DOWNLOAD_SPEED}Mbps down & {MIN_UPLOAD_SPEED}Mbps up? {url}"
        entry_field.send_keys(message)
        # apparently there might be some anti-bot protection happening here, but I couldn't reproduce it
        driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]'
                                     '/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]').click()
        # so it's possible to see the result before closing the window
        time.sleep(10)


driver = webdriver.Chrome()

# get the speed test result
ping, raw_dl, raw_ul, result_url = test_speed()

send_complaint = False
# evaluate the dl and ul speed results
try:
    download_speed = float(raw_dl)
except ValueError as ex:
    # not a particularly elegant way to handle this, but that's really not in the scope of the project
    download_speed = 0
    print(ex)
else:
    if download_speed < MIN_DOWNLOAD_SPEED:
        send_complaint = True

try:
    upload_speed = float(raw_ul)
except ValueError as ex:
    upload_speed = 0
    print(ex)
else:
    if upload_speed < MIN_UPLOAD_SPEED:
        send_complaint = True

# tweet if either/both results are below the "guaranteed" speeds
if send_complaint:
    send_tweet(ping, download_speed, upload_speed, result_url)
else:
    # print the results for reference, it will list "0" speed if there was some issue
    print(f"Ping: {ping}\n"
          f"Download speed: {download_speed}Mbps (guaranteed: {MIN_DOWNLOAD_SPEED}Mbps)\n"
          f"Upload speed: {upload_speed}Mbps (guaranteed: {MIN_UPLOAD_SPEED}Mbps)")

# close the browser window
driver.close()
