import os
import time
import requests
import pandas as pd
from selenium import webdriver
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
    # Set up the WebDriver
    driver = webdriver.Chrome()

    # Navigate to the main Crude Oil Futures page
    url = 'https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html'
    driver.get(url)

    # Wait for the Quotes tab to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "QUOTES"))
    )

    # Click on the Quotes tab
    quotes_tab = driver.find_element(By.LINK_TEXT, "QUOTES")
    quotes_tab.click()

    # table_container_path = "/html/body/main/div/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div/div"
    table_container_path1 = "/html/body/main/div/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div/div/div/div[1]/div[1]/table"
    # Wait for the table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, table_container_path1))
    )

    # Locate the table element
    table = driver.find_element(By.XPATH, table_container_path1)

    # Extract data from table rows
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Loop through rows and columns to extract data
    data = []
    for row in rows[1:]:  # Skip header row
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])

    # Convert to DataFrame for easy manipulation
    df = pd.DataFrame(data, columns=["Month", "Options", "Chart", "Last", "Change", "Prior Settle", "Open", "High", "Low", "Volume", "Updated"])

    # Check if the DataFrame is not empty
    if not df.empty:
        for i in range(1, 15):
            file_name = df.Month[i].split("\n")[0].replace(" ", "_") + ".csv"
            row_df = pd.DataFrame([df.iloc[i]], columns=df.columns)
            if os.path.exists('data/' + file_name):
                existing_df = pd.read_csv('data/' + file_name)
                row_df = pd.concat([existing_df, row_df], ignore_index=True)
            row_df.to_csv('data/' + file_name, index=False)

        print("Futures for the next 15 months have been scraped.")

    else:
        print("The DataFrame is empty. No data was found in the table.")

    # Close the driver
    driver.quit()

# Loop to automate the scraping process every 2 minutes
while True:
    print("Starting data scraping...")
    scrape_data()
    print("Scraping complete. Saving the notebook before the next run.")
    save_notebook()
    print("\nNotebook saved. Waiting for 10 minutes before the next run.")
    time.sleep(600)
