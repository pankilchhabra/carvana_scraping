from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
 
driver = webdriver.Chrome()
driver.get("https://www.carvana.com/cars")
time.sleep(20)

# To extract all companies name
make_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[1]/aside/div/div[1]/div/div/div/div[2]/div[2]/div[1]/p')
make_button.click()
companies = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[1]/aside/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div')
company_list = companies.text.split('\n')

location = driver.find_element(By.XPATH, '//*[@id="search-tools"]/div[1]/div/span').text
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






sample_list = [concatenated_list[0], concatenated_list[1]]
data_to_append = []
n = 1

for url in sample_list:
    driver.get(url)
    time.sleep(25)

    element = driver.find_elements(By.ID, '__next')
    words = element[0].text.split('\n')
    car = ""
    car_name = ""
    company_name = ""
    model = ""
    year = ""
    price = ""
    miles = ""
    car_category = ""
    fuel_type = ""
    auto_man = ""
    VIN = ""
    for i in range(0,len(words)):
        if(re.match(r'\d{1,3}(?:,\d{3})*(?:\.\d+)? miles', words[i])):
            miles = words[i]
        if not price:
            if(re.match(r'\$\d{1,3}(?:,\d{3}){0,2}', words[i])):
                price = words[i]
        if(re.match(r'20\d{2}\s*', words[i])):
            car = words[i]
            car_name = ' '.join(car.split()[1:])
            for company in company_list:
                if(company in car_name):
                    company_name = company
                    model = car_name.replace(company_name, '')
            year = car.split(" ")[0]
            car_category = words[i+1]
        if(words[i].startswith("VIN")):
            VIN = words[i]

        # To do : Improve logic for Fuel and Auto/Manual
        if(words[i]=="Fuel"):
            fuel_type = words[i+1]
        if(words[i]=="Transmission"):
            auto_man = words[i+1]
        if(("Auto" in words[i]) or ("Manual" in words[i])):
            auto_man = words[i]


    data_to_append.append((n, url.replace("#vehicle-details", ''), company_name, model, price, (VIN.split(" ")[1]),  
                            year, miles, car_category, fuel_type, (auto_man.split(',')[0]), location))
    n = n+1
driver.quit()





df = pd.DataFrame(data_to_append, columns=['Sr. no.', 'Link', 'Company', 'Model', 'Price', 'VIN', 'Year', 'Miles', 
                                            'Category', 'Fuel', 'Auto/Manual', 'Location'])
display(df)