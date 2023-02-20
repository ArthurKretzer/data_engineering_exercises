from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

tabela = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]')

with open('print.png', 'wb') as f:
    # create action chain object
    action = ActionChains(driver)
    # Scrolls down the page to full visualize nicholas cage photo. This prevents cropping.
    driver.execute_script("window.scrollTo(0,300)")
    nicholas_cage_photo = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[2]/td/div/div/div/a/img')
    # Takes screenshow as png and writes directly on the file
    f.write(nicholas_cage_photo.screenshot_as_png)

# In oder to read_html interpret the html as a table,
#  we need to include tags at the start and the end of the html.
# The return is always a list. In this case is a list of length 1, so just select the first item.
df = pd.read_html("<table>" + tabela.get_attribute('innerHTML') + "</table>")[0]

print(df)

df.to_csv("nicholas_cage_movies.csv", sep=";", index=False)