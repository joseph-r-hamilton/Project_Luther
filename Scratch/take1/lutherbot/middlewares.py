from scrapy import signals
import re
from scrapy.http import Response
from scrapy.exceptions import IgnoreRequest

from scrapy.http import HtmlResponse
from scrapy.utils.response import get_meta_refresh

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, NoAlertPresentException
import time
import random

from xml.dom import minidom
