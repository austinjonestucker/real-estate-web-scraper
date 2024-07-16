# Real Estate Web Scraper

This repository contains a Python-based web scraper used to pull listing details from a photo card on a housing listing website. It uses Selenium to collect pages of information and parse them into raw data to be further processed in a data analytics capacity.

## Pre-requisites
This program requires a webdriver to be installed and accessible on the PATH of the executing environment. This can be found at [Chrome](https://googlechromelabs.github.io/chrome-for-testing/) or [Firefox](https://github.com/mozilla/geckodriver). Alternatively, tooling like Homebrew (Mac OS), yum/dnf (RHEL-based Linux distributions) & apt (Debian-based Linux distributions) can be used to install the above webdrivers.

## Usage
To use this process, run the following:

```bash
$ export SCRAPER_BROWSER=<chrome or firefox>
$ python web_scraper.py --scrape-url "URL TO BE SCRAPED" --div-class "DIV CLASS WITH REPEATING ELEMENTS" --button-class "BUTTON CLASS WITH NEXT BUTTON"
```
