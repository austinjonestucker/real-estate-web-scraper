from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def extract_nested_values(html_content, definition_file):
    """
    Extracts nested values from HTML content based on a path-like syntax.

    :param html_content: The HTML content as a string.
    :param definition_file: The file path containing paths to search
    :return: List of text content of the matching elements.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = {}

    with open(definition_file, 'r') as path:
        paths = path.readlines()

    for path in paths:
        name_value = path.split('=')[0]
        name_values = name_value.split(',')
        pathway = path.split('=')[1].strip('\n')
        current_elements = [soup]
        # Split the path by '/' to navigate through nested elements
        for part in pathway.split('/'):
            next_elements = []
            tag_class = part.split('.')
            # Each part can be a tag name or a class selector
            for element in current_elements:
                print(tag_class)
                try:
                    next_elements.extend(soup.find_all(tag_class[0], class_=tag_class[1]))
                except TypeError:
                    next_elements = []

            # Update the current elements to the next level
            current_elements = next_elements
            print(current_elements)
        elements.update(dict([(name, element.get_text(strip=True)) for name, element in zip(name_values, current_elements)]))

    # Extract and return the text content from the final elements
    return elements


def extract_body_html(driver):
    return driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
