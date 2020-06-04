import client
import time
import base64
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import config

browser = config.browser
solver = config.solver
pyperclip.copy(client.CPF)

browser.get('https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao')

while True:
    try:
        elem_captcha = browser.find_element_by_xpath("//*[@id='captcha-element']/table/tbody/tr[1]/td[1]/img")
    except NoSuchElementException:
        browser.find_element_by_xpath('/html/body/div[2]/main/div[1]/div/fieldset/button').click()
        time.sleep(3)
        break
    else:
        img_captcha_base64 = browser.execute_async_script("""
                        var elem = arguments[0], callback = arguments[1];
                        elem.addEventListener('load', function fn(){
                          elem.removeEventListener('load', fn, false);
                          var cnv = document.createElement('canvas');
                          cnv.width = this.width; cnv.height = this.height;
                          cnv.getContext('2d').drawImage(this, 0, 0);
                          callback(cnv.toDataURL('image/jpeg').substring(22));
                        }, false);
                        elem.dispatchEvent(new Event('load'));
                        """, elem_captcha)

    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    captcha_text = solver.solve_and_return_solution("captcha.jpg")
    if captcha_text != 0:

        browser.find_element_by_id('numeroDocumentoPesquisado').send_keys(Keys.CONTROL, 'v')

        textocaptcha = browser.find_element_by_id('captcha-input')
        textocaptcha.clear()
        textocaptcha.send_keys(captcha_text)
        browser.find_element_by_id('submit').click()
        try:
            browser.find_element_by_xpath('/html/body/div[2]/main/div[1]/div/fieldset/button').click()
            time.sleep(3)
            break
        except NoSuchElementException:
            print('Não Achei o botao de baixar então vou repetir')
    else:
        print('Deu erro ao resolver o captcha')