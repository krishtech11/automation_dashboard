from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_driver(headless: bool = True) -> WebDriver:
    """Initialize and return a Chrome WebDriver instance."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver: WebDriver, url: str, username: str, password: str) -> Dict[str, Any]:
    """Handle website login."""
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        
        # These selectors are just examples and should be updated based on the target website
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        
        time.sleep(2)  # Wait for login to complete
        
        return {"status": "success", "message": "Successfully logged in"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search(driver: WebDriver, query: str) -> Dict[str, Any]:
    """Perform a search on the current page."""
    try:
        # These selectors are just examples and should be updated based on the target website
        search_box = driver.find_element(By.NAME, "q")
        search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        search_box.clear()
        search_box.send_keys(query)
        search_button.click()
        
        time.sleep(2)  # Wait for search results
        
        # Get search results (example)
        results = driver.find_elements(By.CSS_SELECTOR, ".search-result")
        
        return {
            "status": "success",
            "message": f"Found {len(results)} search results",
            "results_count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def automate_web_interaction(
    url: str, 
    username: Optional[str] = None, 
    password: Optional[str] = None, 
    search_query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main function to handle web automation.
    
    Args:
        url: The URL of the website to interact with
        username: Username for login (if required)
        password: Password for login (if required)
        search_query: Text to search for (if any)
        
    Returns:
        Dict containing the result of the automation
    """
    driver = None
    try:
        driver = init_driver()
        result = {}
        
        if username and password:
            login_result = login(driver, url, username, password)
            result["login"] = login_result
            if login_result.get("status") == "error":
                return result
        else:
            driver.get(url)
            time.sleep(2)  # Wait for page to load
        
        if search_query:
            search_result = search(driver, search_query)
            result["search"] = search_result
        
        result["status"] = "success"
        result["message"] = "Web automation completed successfully"
        
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if driver:
            driver.quit()
