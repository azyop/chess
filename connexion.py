import pickle
import time

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def connection(driver):
    cookies_file = "cookies.pkl"
    driver.get("https://www.chess.com/home")
    load_cookie(driver, cookies_file)
    return driver

def reconnect(driver):
    driver.get("https://www.chess.com/login")
    user = "username"
    pwd = "pass"
    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(user)
    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(pwd)
    time.sleep(2)
    driver.find_element_by_id("login").click()
    time.sleep(2)
    save_cookie(driver, "cookies.pkl")
    return driver
