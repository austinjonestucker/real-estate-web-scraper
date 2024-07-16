from selenium.webdriver.common.by import By


def extract_body_html(driver):
    return driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
