import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_notebook():
    """
    Save the current Jupyter notebook programmatically using Jupyter's REST API.
    """
    try:
        # Get the current notebook's name and path
        notebook_name = os.path.basename(os.getcwd()) + '.ipynb'
        
        # Jupyter notebook server API
        server_url = "http://localhost:8888"  # Change this if you're using a different port
        api_url = f"{server_url}/api/contents/{notebook_name}"
        
        # Send a request to the Jupyter server to save the notebook
        response = requests.patch(api_url, json={'type': 'notebook'}, headers={"Authorization": f"token {os.environ.get('JUPYTER_TOKEN')}"})
        
        if response.status_code == 200:
            print("Notebook saved successfully!")
        else:
            print(f"Failed to save notebook: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while trying to save the notebook: {e}")

def scrape_data():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Set up the ChromeDriver path
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the main Crude Oil Futures page
        url = 'https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.quotes.html'
        driver.get(url)
        
        # print('-> Accessed the main page')

        # # Wait for the Quotes tab to be clickable
        # WebDriverWait(driver, 30).until(
        #     EC.element_to_be_clickable((By.LINK_TEXT, "QUOTES"))
        # )
        # print('-> Accessed the Quotes tab icon')

        # # Click on the Quotes tab
        # quotes_tab = driver.find_element(By.LINK_TEXT, "QUOTES")
        # quotes_tab.click()
        print('-> Accessed the Quotes tab page')

        # table_container_path = "/html/body/main/div/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div/div"
        table_container_path1 = "/html/body/main/div/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div/div/div/div[1]/div[1]/table"
        # Wait for the table to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, table_container_path1))
        )
        print('-> Loaded the table')

        # Locate the table element
        table = driver.find_element(By.XPATH, table_container_path1)
        print('-> Located the table')

        # Extract data from table rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        print('-> Extracted data from table')

        # Loop through rows and columns to extract data
        data = []
        for row in rows[1:]:  # Skip header row
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([col.text for col in cols])

        # Convert to DataFrame for easy manipulation
        df = pd.DataFrame(data, columns=["Month", "Options", "Chart", "Last", "Change", "Prior Settle", "Open", "High", "Low", "Volume", "Updated"])

        data_dir = '/home/arshia_gururaj/data'

        # Ensure the 'data' directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Created directory at {data_dir}")

        # Check if the DataFrame is not empty
        if not df.empty:
            for i in range(1, 7):
                file_name = df.Month[i].split("\n")[0].replace(" ", "_") + ".csv"
                row_df = pd.DataFrame([df.iloc[i]], columns=df.columns)
                if os.path.exists('data/' + file_name):
                    existing_df = pd.read_csv('data/' + file_name)
                    row_df = pd.concat([existing_df, row_df], ignore_index=True)
                row_df.to_csv('data/' + file_name, index=False)
            print("Futures for the next 6 months have been scraped.")
        else:
            print("The DataFrame is empty. No data was found in the table.")

        # Close the driver
        driver.quit()

    except Exception as e:
        print(f"An error occurred while scraping data: {e}")

# Loop to automate the scraping process every 2 minutes
while True:
    print("Starting data scraping...")
    scrape_data()
    print("Scraping complete. Saving the notebook before the next run.")
    try:
        save_notebook()
    except Exception as e:
        print(f"Could not save the notebook: {e}")
    print("Notebook saved. Waiting for 10 minutes before the next run.")
    time.sleep(600)
