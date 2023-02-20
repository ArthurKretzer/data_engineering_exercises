from selenium import webdriver
from selenium.webdriver.common.by import By

import sys

cep = sys.argv[1]

if cep:
    driver = webdriver.Chrome()

    driver.get("https://buscacepinter.correios.com.br/app/endereco/index.php?t")
    element_cep = driver.find_element(By.NAME, "endereco")
    element_cep.clear()
    element_cep.send_keys(cep) 

    element_combo = driver.find_element(By.NAME, "tipoCEP")
    element_combo.click()
    element_combo.find_element(By.XPATH, "//*[@id='tipoCEP']/optgroup/option[6]").click()

    driver.find_element(By.ID, "btn_pesquisar").click()
    driver.implicitly_wait(1)
    logradouro = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[1]')
    bairro = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[2]')
    cidade = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[3]')

    print(f'''
    Para o cep: {cep}\n
    logradouro: {logradouro.text.split(' - ')[0]}\t
    bairro: {bairro.text}\t
    cidade: {cidade.text}
    ''')