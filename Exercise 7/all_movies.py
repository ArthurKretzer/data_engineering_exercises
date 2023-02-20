from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

tabela = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]')

# In oder to read_html interpret the html as a table,
#  we need to include tags at the start and the end of the html.
# The return is always a list. In this case is a list of length 1, so just select the first item.
df = pd.read_html("<table>" + tabela.get_attribute('innerHTML') + "</table>")[0]

print(df)

df.to_csv("nicholas_cage_movies.csv", sep=";", index=False)