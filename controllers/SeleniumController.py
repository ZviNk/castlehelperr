from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from collections import deque
import time
import pyotp

from const import FORUM_BASE_URL, FORUM_LOGIN, FORUM_PASS, FORUM_GAUTH_KEY


class SeleniumController:
    def __init__(self):
        self.command_queue = deque()
        self.driver = webdriver.Chrome()  # Используйте свой выбор драйвера

    def login_forum(self):
        self.driver.get(FORUM_BASE_URL)
        time.sleep(10)
        username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="login"]')
        username_input.clear()
        username_input.send_keys(FORUM_LOGIN)

        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.clear()
        password_input.send_keys(FORUM_PASS)

        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        # Генерация кода от Google Authenticator
        totp = pyotp.TOTP(FORUM_GAUTH_KEY)  # Вставьте свой секретный ключ
        code = totp.now()

        # Ввод кода от Google Authenticator
        code_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="code"]')
        code_input.send_keys(code)

        # Нажатие кнопки подтверждения
        confirm_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_button.click()

        # Получение куки
        time.sleep(3)
        cookies = self.driver.get_cookies()
        xf_user = None
        xf_tfa_trust = None
        xf_session = None
        xf_csrf = None
        for cookie in cookies:
            print(f"name: {cookie['name']} | value: {cookie['value']}")
            if cookie['name'] == 'xf_user':
                xf_user = cookie['value']
            elif cookie['name'] == 'xf_tfa_trust':
                xf_tfa_trust = cookie['value']
            elif cookie['name'] == 'xf_session':
                xf_session = cookie['value']
            elif cookie['name'] == 'xf_csrf':
                xf_csrf = cookie['value']
        return {
            "xf_user": xf_user,
            "xf_tfa_trust": xf_tfa_trust,
            "xf_session": xf_session,
            "xf_csrf": xf_csrf
        }