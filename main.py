from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import pickle
import os
import dotenv

def login(driver):
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
        print('Logged in by cookies')
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

    # save cookies
    pickle.dump(driver.get_cookies(), open('instagram_cookies.pkl', 'wb'))
    print('Cookies saved to instagram_cookies.pkl')
    print('Logged in')

def load_cookies(driver):
    if os.path.exists('instagram_cookies.pkl'):
        cookies = pickle.load(open('instagram_cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        return

def send_message(driver, message: str):
    try:
        textbox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )
        textbox.send_keys(message)
        textbox.send_keys(Keys.RETURN)

    except:
        print('Error: Cannot find textbox')


if __name__ == "__main__":
    dotenv.load_dotenv()

    browser = str(os.getenv('BROWSER'))
    if browser == 'edge':
        driver = webdriver.Edge()
    else:
        driver = webdriver.Chrome()

    login(driver)

    TARGET_URL = str(os.getenv('TARGET_URL'))
    driver.get(TARGET_URL)

    SEND_DELAY = int(str(os.getenv('SEND_DELAY')))
    with open('message.txt', 'r') as f:
        messages = f.readlines()
        for message in messages:
            print(f'Message: {message}')
            # send_message(driver, message)
            time.sleep(SEND_DELAY) # delay between each message

    driver.quit()
