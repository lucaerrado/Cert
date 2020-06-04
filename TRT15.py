import client
import time
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import config

browser = config.browser
solver = config.solver

browser.get('https://ceat.trt15.jus.br/ceat/certidaoAction.seam')

search_field = wait(browser, 5).until(
                EC.presence_of_element_located((By.ID, "certidaoActionForm:j_id23:doctoPesquisa")))

browser.find_element_by_id('certidaoActionForm:j_id23:doctoPesquisa').send_keys(client.CPF)

while True:

    try:
        elem_captcha = browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/form/div/div[2]/div[2]/div[4]/div/span[1]/img')
    except NoSuchElementException:
        browser.find_element_by_id('certidaoActionForm:certidaoActionImprimir').click()
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
        textocaptcha = browser.find_element_by_id('certidaoActionForm:j_id51:verifyCaptcha')
        textocaptcha.clear()
        textocaptcha.send_keys(captcha_text)
        browser.find_element_by_id('certidaoActionForm:certidaoActionEmitir').click()
        try:
            browser.find_element_by_id('certidaoActionForm:certidaoActionImprimir').click()
            time.sleep(3)
            break
        except NoSuchElementException:
            print('ola')

    else:
        print("task finished with error " + solver.error_code)