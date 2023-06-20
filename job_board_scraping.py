import pandas as pd

#using Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

#load driver, get the correct webpage, and set this page as current tab
driver = webdriver.Chrome('./chromedriver')
driver.get("https://realpython.github.io/fake-jobs/")
original_tab = driver.current_window_handle

#create a function to get elements from the page based on their class name and add to an empty list
def create_col(class_name):
    list = driver.find_elements(By.CLASS_NAME, class_name)
    column = [item.text for item in list]
    return column

#call the function for the 4 key pieces of info i want to collect
job_title = create_col("is-5")
hiring_company = create_col("is-6")
job_location = create_col("location")
date = create_col("is-small")

#combine the 4 lists into a dataframe
job_table = pd.DataFrame({
    "Job Title" : job_title,
    "Hiring Company" : hiring_company,
    "Job Location" : job_location,
    "Date posted" : date
})

#save an empty list for the job descriptions
job_descriptions = []

#create a list of links to loop through. for each link: click it, change tab, add 
#cleaned text to empty job descriptions list then close tab and switch back to main window
links = driver.find_elements(By.LINK_TEXT, "Apply")
#used a break limit for testing which is commented out
# i = 1
for link in links:
    # i = i+1
    link.click()

    for window_handle in driver.window_handles:
        if window_handle != original_tab:
            driver.switch_to.window(window_handle)
            break

    job_descriptions.append(driver.find_element(By.CLASS_NAME, "content").text.rsplit("Location", 1)[0].strip())
    driver.close()
    driver.switch_to.window(original_tab)
    # if i == 3:
    #     break

#quit the driver
driver.quit()

#add the job descriptions list to the job table
job_table["Job Description"] = job_descriptions

job_table.to_csv("Jobs Info Table.csv")