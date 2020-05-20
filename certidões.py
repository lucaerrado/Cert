from selenium import webdriver
from anticaptchaofficial.imagecaptcha import *
import time

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key("060e9da0cfca5c0473793d11a269d236")

browser = webdriver.Chrome('C://Users//Adm07//Desktop//chromedriver')
browser.get('https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao')
searchbar = browser.find_element_by_id('numeroDocumentoPesquisado')
searchbar.send_keys('5127')
time.sleep(.050)
searchbar.send_keys('058588')
time.sleep(.050)
searchbar.send_keys('6')
captcha_text = solver.solve_and_return_solution("C://Users//Adm07//Desktop//screenshot_1.png")
if captcha_text != 0:
    print ("captcha text "+captcha_text)
else:
    print ("task finished with error "+solver.error_code)