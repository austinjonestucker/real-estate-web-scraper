import os
import json
import argparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from parser import extract_body_html, extract_nested_values

SCRAPER_BROWSER = os.environ.get("SCRAPER_BROWSER")


def extract_href_from_anchor_in_div(driver, cls):
    return driver.find_elements(By.XPATH, f"//div[@class='{cls}']/a[@href]")


def extract_button_directly(driver, cls):
    return driver.find_element(By.XPATH, f"//button[@class='{cls}']")


def extract_button_from_anchor(driver, cls, anchor_cls, span_class):
    button_xpath = f"//div[@class='{cls}']/a[@class='{anchor_cls}']"
    return driver.find_element(By.XPATH, button_xpath)


def extract_links_from_photo_cards(driver, div_class, output_file):
    # find the photo cards on the page and get the links
    photo_cards = extract_href_from_anchor_in_div(driver, div_class)
    with open(output_file, "a+") as file:
        for photo_card in photo_cards:
            file.write(f"{photo_card.get_attribute('href')}\n")


def navigate_and_extract_links(
    driver, div_class, links_file, button_class=None, anchor_class=None, span_class=None
):
    # clear links file each run
    if os.path.exists(links_file):
        os.remove(links_file)
    # Extract photo cards on first page
    extract_links_from_photo_cards(driver, div_class, links_file)
    actions = ActionChains(driver)
    # Continue to click on next button and extract photo card links until
    # next button can no longer be clicked
    while True:
        try:
            # Determine button type, based on passed in parameters
            if button_class and anchor_class and span_class:
                button = extract_button_from_anchor(
                    driver,
                    button_class,
                    anchor_class,
                    span_class,
                )
            elif button_class:
                button = extract_button_directly(driver, button_class)
            else:
                raise "button not implemented"
            # move to button and click
            actions.move_to_element(button)
            button.click()
            extract_links_from_photo_cards(driver, div_class, links_file)
        except NoSuchElementException:
            # button is not on page anymore
            print("no button found")
            break


def get_page_details(
    driver, links_file, definition_file, output_file
):
    link_file = open(links_file, "r")
    # clear links file each run
    if os.path.exists(output_file):
        os.remove(output_file)
    data_file = open(output_file, "a")
    link = link_file.readline()
    # iterate through links
    while link:
        # get link
        driver.get(link)
        # get html from link,
        html = extract_body_html(driver)
        # parse and extract data locally
        elements = extract_nested_values(html, definition_file)
        # write to file
        json.dump(elements, data_file)
        data_file.write("\n")
        # data_file.write('\n'.join(elements))
        link = link_file.readline()


if __name__ == "__main__":
    if SCRAPER_BROWSER == "chrome":
        driver = webdriver.Chrome()
    elif SCRAPER_BROWSER == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("unsupported driver")
    parser = argparse.ArgumentParser(prog="house_prices_web_scraper")
    parser.add_argument("--scrape-url", dest="scrape_url")
    parser.add_argument("--div-class", dest="div_class")
    parser.add_argument("--button-class", dest="button_class")
    parser.add_argument("--anchor-class", dest="anchor_class")
    parser.add_argument("--span-class", dest="span_class")
    parser.add_argument("--output-file", dest="output_file")
    parser.add_argument(
        "--resource-definition-file", dest="resource_definition"
    )
    args = parser.parse_args()

    links_file = "./links.txt"
    driver.get(args.scrape_url)
    # navigate_and_extract_links(
    #     driver,
    #     args.div_class,
    #     links_file,
    #     args.button_class,
    #     args.anchor_class,
    #     args.span_class,
    # )
    get_page_details(
        driver,
        links_file,
        args.resource_definition,
        args.output_file,
    )
    driver.close()
    driver.quit()
