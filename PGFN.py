import config
import client
import time
import base64
from selenium.common.exceptions import NoSuchElementException

browser = config.browser
solver = config.solver

browser.get('http://servicos.receita.fazenda.gov.br/Servicos/certidao/CNDConjuntaInter/EmiteCertidaoInternet.asp?Tipo'
            '=2&NI=' + client.CPF + '&passagens=0')

while True:

    try:
        elem_captcha = browser.find_element_by_xpath("/html/body/p/table/tbody/tr/td/p/table/tbody/tr/td/form/font["
                                                     "2]/table[2]/tbody/tr/td[3]/font/img")
        pesquisa = browser.find_element_by_xpath('/html/body/p/table/tbody/tr/td/p/table/tbody/tr/td/form/input[1]')
        pesquisa.clear()
        pesquisa.send_keys(client.CPF)

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
    except NoSuchElementException:
        try:
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/b/p/table/tbody/tr/td/font/a[2]').click()
            browser.find_element_by_xpath('/html/body/div[3]/table/tbody/tr/td[2]/a/img').click()
            browser.execute_script('window.print();')
            break
        except NoSuchElementException:
            browser.execute_script('window.print();')
            time.sleep(3)
            break
    while True:

        captcha_text = solver.solve_and_return_solution("captcha.jpg")
        if captcha_text != 0:
            captcha = browser.find_element_by_xpath('/html/body/p/table/tbody/tr/td/p/table/tbody/tr/td/form/font[2]/table[2]/tbody/tr/td[2]/font/input')
            captcha.clear()
            captcha.send_keys(captcha_text)
            browser.find_element_by_xpath('/html/body/p/table/tbody/tr/td/p/table/tbody/tr/td/form/input[2]').click()
            try:
                try:
                    alert = browser.switch_to.alert
                    alert.accept()
                except:
                    browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/b/p/table/tbody/tr/td/font/a[2]').click()
                    browser.execute_script('window.print();')
                    time.sleep(1)
                    break
            except NoSuchElementException:
                browser.execute_script('window.print();')
                time.sleep(1)
                break
    else:
        print("task finished with error " + solver.error_code)