from tqdm import tqdm
import pandas as pd
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# setup chrome options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
driver = uc.Chrome(options=chrome_options)
driver.set_page_load_timeout(30)
# Load the Excel file into a pandas DataFrame
file_path = 'kritikos_7k_update.xlsx'
df = pd.read_excel(file_path)

# Add "Key Code" and "Description" columns if they don't exist
if 'Key Code' not in df.columns:
    df['Key Code'] = ''
if 'Description' not in df.columns:
    df['Description'] = ''


# Iterate over each row in the DataFrame
for index, row in tqdm(df.iloc[20:1000].iterrows()):
    try:
        product_url = row['URL of product']  # Adjust the column name as per your Excel file
        
        # Visit the product page
        driver.get(product_url)
        
        # Scrape the Key Code and Description (update the XPaths accordingly)
        try:
            key_code = driver.find_element(By.CSS_SELECTOR, 'p.ProductDetails_productCode___TLkS').text.strip()
            # Extract the product code by splitting at "Κωδ. προϊόντος" and taking the part after it
            key_code = key_code.split("Κωδ. προϊόντος")[-1].strip()
        except Exception as e:
            key_code = ''
        try:
            description = driver.find_element(By.CSS_SELECTOR, 'p.ProductDetails_desciptionText__5DU4_').text.strip()
        except Exception as e:
            description = ''
            

        # Update the DataFrame
        df.at[index, 'Key Code'] = key_code
        df.at[index, 'Description'] = description
    except Exception as e:
        print("Exception in .get")
        time.sleep(10)
        continue
# Save the updated DataFrame back to the Excel file
df.to_excel(file_path, index=False)

# Close the browser
driver.quit()