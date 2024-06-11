# Importing Important libraires
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
from colorama import Fore  # Import Fore for text color

# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")   # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--window-size=1920,1080")  # Set window size to ensure all elements are loaded
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass automation detection
chrome_options.add_argument("--log-level=3")  # Suppress logging
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images in headless mode to save resources

# Setup webdriver with ChromeDriverManager
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

def search_game(driver, game_name):
    driver.get("https://fitgirl-repacks.site/")

    # Wait for home page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "header-main"))
    )

    # Click the search toggle button to get search option
    toggle_search = driver.find_element(By.CLASS_NAME, "search-toggle")
    driver.execute_script("arguments[0].click();", toggle_search)

    # Wait for the search bar to become visible after clicking the toggle
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "s")))

    # Locate the search bar again after clicking the toggle
    search = driver.find_element(By.NAME, "s")
    search.send_keys(game_name)

    # Click submit query button
    search_submit = driver.find_element(By.CLASS_NAME, "search-submit")
    driver.execute_script("arguments[0].click();", search_submit)
        
   
    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content")))

    # Find the first 5 search results and print their link text
    search_results = driver.find_elements(By.CSS_SELECTOR, ".entry-title a")
    if search_results:
        print(f"\n{Fore.WHITE}Search Results:{Fore.RESET}")
        search_results_text = [result.text for result in search_results[:5]]
        for i, result_text in enumerate(search_results_text, start=1):
            # Generate random color for each result
            color = Fore.LIGHTBLUE_EX
            print("")
            print(f"{color}{i}. {result_text}")
        return search_results[:5], search_results_text
    else:
        print("\nNo search results found\nMake sure the Game name you entered is correct and try again\n")
        return None, None

while True:
    # Taking user input, the game name
    game_name = input("\nEnter Game Name: ")
    
    # Search for the game
    search_results, search_results_text = search_game(driver, game_name)
    
    # If results are found, break the loop
    if search_results:
        break

# Ask the user to select one of the results
while True:
    try:
        selection = int(input(f"\n{Fore.WHITE}Select the result number you want to continue with (1-5): {Fore.RESET}"))
        if 1 <= selection <= len(search_results):
            break
        else:
            print("Please enter a number between 1 and 5.")
    except ValueError:
        print("Please enter a valid number.")

# Click the selected search result
selected_result_text = search_results_text[selection - 1]
selected_result_link = driver.find_element(By.LINK_TEXT, selected_result_text)
driver.execute_script("arguments[0].click();", selected_result_link)
print(f"\n{Fore.WHITE}Selected result: {selected_result_text}\n")
print("                                         Download Links")

# Wait for the page downloading links to load on page
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "entry-content"))
)

# Get the HTML content of the page
html_content = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <li> tags and extract the links with specific keywords
for li in soup.find_all('li'):
    a_tag = li.find('a')
    if a_tag:
        link = a_tag['href']
        if "Filehoster" in li.text or "1377x" in li.text or "Tapochek.net" in li.text or ".torrent file only" in li.text:
            website_name = a_tag.text.strip()
            if website_name:
                # Generate random color for each link
                color = Fore.GREEN
                print(f"\n{Fore.WHITE}Website Name: {Fore.LIGHTMAGENTA_EX}{website_name.strip()}{Fore.RESET} | Link: {color}{link}{Fore.RESET}")

# Close the browser
driver.quit()
