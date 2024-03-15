from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
 
driver = webdriver.Chrome()
driver.get("https://www.carvana.com/cars")
time.sleep(20)

element = driver.find_elements(By.XPATH, "//a[@href]")

links = []
pattern = re.compile(r'https://www.carvana.com/vehicle/\d+')

for i in element:
    links.append(i.get_attribute("href"))
filtered_list = [item for item in links if pattern.match(item)]
concatenated_list = [item + "#vehicle-details" for item in filtered_list]

'''
base_url = 'https://www.carvana.com/cars?page='
# Considering 2 to 5 pages only
page_list = set([base_url + str(page_number) for page_number in range(2, 6)])

for i in page_list:
    print(page_list)
'''





data_to_append = []

for url in concatenated_list:
    driver.get(url)
    time.sleep(40)

    element = driver.find_elements(By.ID, '__next')
    words = element[0].text.split('\n')
    car = words[12]
    car_name = ' '.join(car.split()[1:])
    year = car.split(" ")[0]
    miles = words[21]
    price = words[14]
    fuel_type = ""
    auto_man = ""
    for i in range(0,len(words)):
        if(words[i]=="Fuel"):
            fuel_type = words[i+1]
        if(words[i]=="Transmission"):
            auto_man = words[i+1]
        if(("Auto" in words[i]) or ("Manual" in words[i])):
            auto_man = words[i]
        if(words[i].startswith("VIN")):
            VIN = words[i]
    data_to_append.append((url,car_name,price,(VIN.split(" ")[1]),year,miles,fuel_type,(auto_man.split(',')[0])))
driver.quit()






df = pd.DataFrame(data_to_append, columns=['Link', 'Car','Price','VIN','Year','Miles','Fuel','Auto/Manual'])
display(df)