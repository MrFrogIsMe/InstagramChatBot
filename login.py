from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import dotenv
import os

def login(driver: webdriver.Edge):
    dotenv.load_dotenv()

    username = str(os.getenv('INSTAGRAM_USERNAME'))
    password = str(os.getenv('INSTAGRAM_PASSWORD'))
    url = str(os.getenv('TARGET_URL'))

    # if cookies exist, load cookies

    driver.get(url)
    if os.path.exists('instagram_cookies.pkl'):
        cookies = pickle.load(open('instagram_cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        print('Logged in')
        return

    try:
        username_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_input = driver.find_element(By.NAME, 'password')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
        login_button.click()

        try:
            save_login = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="儲存資料"]'))
            )
            save_login.click()

        except:
            print('Error: Cannot find login button')

    except:
        print('Error: Cannot find username or password input')

    notification_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="稍後再說"]'))
    )
    if notification_button:
        notification_button.click()

    # save cookies
    pickle.dump(driver.get_cookies(), open('instagram_cookies.pkl', 'wb'))
    print('Cookies saved to instagram_cookies.pkl')
    print('Logged in')

def load_cookies(driver: webdriver.Edge):
    if os.path.exists('instagram_cookies.pkl'):
        cookies = pickle.load(open('instagram_cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        return
