import time
import os
import json
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
    log('Logging in user')
    
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

def scrap_details():
    log('Scraping details')
    wait = WebDriverWait(driver, 5)
    jobs = []
    wait.until(ec.visibility_of_any_elements_located((By.CSS_SELECTOR, "li.jobs-search-results__list-item.occludable-update.p0.relative.ember-view"))) 
    jobs_list = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
    log(f"Jobs found: {len(jobs_list)}")
    for job in jobs_list:
        title = job.find_element(By.XPATH, ".//div/div/div/div[2]/div[1]/a").text
        jobs.append({'title': title})
        
    return jobs


def log(msg):
    print(f'===== {msg} =====')
 

""" ==================== MAIN EXECUTION ==================== """

try:
    # Pre-configuration
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Opening the site
    driver = init_driver(headless=False)

    # Logging in the user
    linkedin_login_user()
    log(f"User {os.environ.get('LINKEDIN_USERNAME')} logged in")

    # Navigating to LinkedIn job search with custom keywords and location
    keywords = ['backend', 'programador', 'java']
    location = 'Spain'
    browse_linkedin_jobs(keywords, location)

    # Scraping jobs details
    jobs = scrap_details()
    print(jobs)
    
finally:
    print('===== Closing the driver =====')
    # Closing the driver 
    driver.close()