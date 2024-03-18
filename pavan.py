l1 = '//*[@id="vehicle-details"]/section/div/div/ul'  # old_page
l2 = '//*[@id="vehicle-details"]/section/div/div[1]'  # New_page

    # Determine which XPath expression to use based on the condition
    # Determine which XPath expression to use based on the condition
xpath_to_use = l1 if len(driver.find_elements(By.XPATH, l1)) > 0 else l2
print(xpath_to_use)

c_auto_manual = driver.find_elements(By.XPATH, xpath_to_use)

    # Create an empty list to store the results
c_vin = []
car_vin = []
car_auto_vs_manual = []
    
    # Check if the new page layout is used
if l2 == xpath_to_use:
        # Extract VIN elements
    vin_element = driver.find_element(By.XPATH, '//span[@class="ml-md font-bold"]')
    c_vin.append(vin_element.text)
    print('New page layout')
    print(c_vin)
else:
        # No VIN found for old page layout
    c_vin.append('0')

#Loop through the elements found and print their visible text
c_automanual = []
for type_a_m in c_auto_manual:
        #print(type_a_m.text)  # This will print the visible text of the WebElement
    c_automanual.append(type_a_m.text)
    

car_vin.append(c_vin)
car_auto_vs_manual.append(c_automanual)
