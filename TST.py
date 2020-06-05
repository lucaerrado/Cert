import config
from anticaptchaofficial.recaptchav2proxyless import *
import time
import client

browser = config.browser
solver = config.solver

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("6fbe461d71186c258bec2e8d8c9b967e")
solver.set_website_url("https://cndt-certidao.tst.jus.br/inicio.faces")
solver.set_website_key("6LeKKAoUAAAAAJwv60Xf2N9-8Ri2mVJVp6dQaw6H")

browser.get('https://cndt-certidao.tst.jus.br/inicio.faces')

browser.find_element_by_xpath('/html/body/form/div/div/div[2]/input[1]').click()

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print ("g-response: "+g_response)
    element = browser.find_element_by_xpath(
        "/html/body/form/div/fieldset/div[1]/table/tbody/tr[2]/td[2]/div/div/textarea")
    browser.execute_script(
        "arguments[0].setAttribute('style', 'width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none;')",
        element)
    browser.find_element_by_xpath('/html/body/form/div/fieldset/div[1]/table/tbody/tr[2]/td[2]/div/div/textarea').send_keys(g_response)
    browser.find_element_by_id('gerarCertidaoForm:cpfCnpj').send_keys(client.CPF)
    browser.find_element_by_id('gerarCertidaoForm:btnEmitirCertidao').click()
    time.sleep(3)
else:
    print ("task finished with error "+solver.error_code)


