import time
import os
from os.path import join, dirname
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv


# Returns an initialized and configured Chrome driver
def init_driver(headless):
    chrome_options = Options()
    if headless: chrome_options.add_argument("--headless")
    if headless: chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=chrome_options)    

# Logs in the user on LinkedIn
def linkedin_login_user():
    print('===== Logging in user =====')
    
    # Navigating to the signin page
    driver.get('https://www.linkedin.com/login?fromSignIn=true&amp;trk=guest_homepage-basic_nav-header-signin')
    
    # Filling in the login info
    input_username = driver.find_element(By.ID, 'username')
    input_username.send_keys(os.environ.get("LINKEDIN_USERNAME"))
    input_password = driver.find_element(By.ID, 'password')
    input_password.send_keys(os.environ.get("LINKEDIN_PASSWORD"))
    
    # Clicking on the sign in button
    button_signin = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[1]/form/div[3]/button")
    button_signin.click()
    
def browse_linkedin_jobs(keywords, location):    
    linkedin_url = get_linkedin_url(keywords, location)
    driver.get(linkedin_url)

# Returns a LinkedIn job URL with the keywords passed in the arguments
def get_linkedin_url(keywords, location):    
    keywords_string = ''
    for index, keyword in enumerate(keywords):
        keywords_string += keyword
        if (index + 1) != len(keywords):
            keywords_string += '%20OR%20'
    linkedin_url = f'https://www.linkedin.com/jobs/search/?currentJobId=2921025191&geoId=105646813&keywords={keywords_string}&location={location}'
    return linkedin_url
 

""" ==================== MAIN EXECUTION ==================== """

# Pre-configuration
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Opening the site
driver = init_driver(headless=False)

# Logging in the user
linkedin_login_user()

# Navigating to LinkedIn job search with custom keywords and location
keywords = ['backend', 'programador', 'java']
location = 'Spain'
browse_linkedin_jobs(keywords, location)

# Closing the driver 
time.sleep(10)
driver.close()