from selenium import webdriver
from anticaptchaofficial.imagecaptcha import *

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key("6fbe461d71186c258bec2e8d8c9b967e")

chrome_options = webdriver.ChromeOptions()
settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}], "selectedDestinationId": "Save as PDF", "version": 2}
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')

browser = webdriver.Chrome(r"chromedriver.exe", options=chrome_options)
