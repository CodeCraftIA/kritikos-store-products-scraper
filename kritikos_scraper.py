import pandas as pd
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from tqdm import tqdm

#manaviki
#fresko kreas
#alantika
#Τυροκομικά
#galaktokomika
#eidh-psugeiou
#katapsuxh
#pantopolio
#kaba
#proswpikh-frontida
#brefika
#kathariothta
#oikiakh-xrhsh
#pet-shop
#biologikaleitourgika
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

#url = "https://kritikos-sm.gr/categories/manabikh/"
#category_initial = "Βιολογικά/Λειτουργικά > "

url_category = [
    ("https://kritikos-sm.gr/categories/manabikh/", "Μαναβική > "),
    ("https://kritikos-sm.gr/categories/fresko-kreas/", "Φρέσκο Κρέας > "),
    ("https://kritikos-sm.gr/categories/allantika/", "Αλλαντικά > "),
    ("https://kritikos-sm.gr/categories/turokomika/", "Τυροκομικά > "),
    ("https://kritikos-sm.gr/categories/galaktokomika/", "Γαλακτοκομικά > "),
    ("https://kritikos-sm.gr/categories/eidh-psugeiou/", "Είδη Ψυγείου > "),
    ("https://kritikos-sm.gr/categories/katapsuxh/", "Κατάψυξη > "),
    ("https://kritikos-sm.gr/categories/pantopwleio/", "Παντοπωλείο > "),
    ("https://kritikos-sm.gr/categories/kaba/", "Κάβα > "),
    ("https://kritikos-sm.gr/categories/proswpikh-frontida/", "Προσωπική Φροντίδα > "),
    ("https://kritikos-sm.gr/categories/brefika/", "Βρεφικά > "),
    ("https://kritikos-sm.gr/categories/kathariothta/", "Καθαριότητα > "),
    ("https://kritikos-sm.gr/categories/oikiakh-xrhsh/", "Οικιακή Χρήση > "),
    ("https://kritikos-sm.gr/categories/pet-shop/", "Pet Shop > "),
    ("https://kritikos-sm.gr/categories/biologikaleitourgika/", "Βιολογικά/Λειτουργικά > "),
]

driver.get("https://kritikos-sm.gr/")

time.sleep(20)
titles=[]
prices= []
detailed_prices=[]
images=[]
urls = []
categories = []
# Function to click the "Load more" button
def load_more(scroll_pause_time=5, max_scroll_attempts=3):
    """
    Scroll to the bottom of a dynamically loading page.
    
    Parameters:
    - driver: The Selenium WebDriver instance.
    - scroll_pause_time: Time to wait after each scroll to load content (in seconds).
    - max_scroll_attempts: Maximum number of scroll attempts before stopping.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load the page content
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # Increment the attempt counter if no new content is loaded
            scroll_attempts += 1
        else:
            # Reset the attempt counter if new content is loaded
            scroll_attempts = 0

        # Break the loop if maximum scroll attempts reached without loading new content
        if scroll_attempts >= max_scroll_attempts:
            break
        
        # Update the last height
        last_height = new_height

def scrape(url_category):
    for url, category_initial in tqdm(url_category):
        driver.get(url)
        time.sleep(10)
        load_more()
        time.sleep(10)

        content = driver.find_element(By.CSS_SELECTOR, "div.ProductMenu_infiniteList__8zE3B.ProductMenu_notSticky__Q5FIP")

        categories1 = content.find_elements(By.CSS_SELECTOR, "div.ProductMenu_categoryContainer__TQ0Xh")

        for category in categories1:
            try:
                cat = category.find_element(By.CSS_SELECTOR, "h1.ProductMenu_listTitle__PxrUW").text.strip()
                cat_full = category_initial + " " + cat
            except Exception as e:
                cat_full = category_initial
            cards = category.find_elements(By.CSS_SELECTOR, "div.ProductListItem_productItem__cKUyG")
            for card in cards:
                try:
                    # Get the title of the product
                    title = card.find_element(By.CSS_SELECTOR, "p.ProductListItem_title__e6MEz").text.strip()
                except Exception as e:
                    title = ""
                try:
                    # Get the detailed price (this includes both the per unit price and any additional weight information)
                    detailed_price = card.find_element(By.CSS_SELECTOR, "p.ProductListItem_description__DRAGa").text.strip()
                except Exception as e:
                    detailed_price = ""
                try:
                    # Get the price (the final price)
                    price = card.find_element(By.CSS_SELECTOR, "p.ProductListItem_finalPrice__sEMjs").text.strip()
                except Exception as e:
                    price = ""
                try:
                    # Get the product URL
                    product_url = card.find_element(By.CSS_SELECTOR, "a.ProductListItem_productLink__BZo3P").get_attribute("href")
                except Exception as e:
                    product_url = ""
                try:
                    # Get the image URL
                    image_url = card.find_element(By.CSS_SELECTOR, "img.ProductListItem_productImage__HbseK").get_attribute("src")
                except Exception as e:
                    image_url = ""

                # Append the scraped data to the corresponding lists
                titles.append(title)
                detailed_prices.append(detailed_price)
                prices.append(price)
                urls.append(product_url)
                images.append(image_url)
                categories.append(cat_full)
        
    # Close the WebDriver
    driver.quit()

    def write_excel(path):
        # Create DataFrame
        df = pd.DataFrame({
            'URL of product': urls,
            'Title': titles,
            'Category': categories,
            'Price': prices,
            'Detailed Price': detailed_prices,
            'Image URL': images,
        })
        # Write DataFrame to Excel
        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            print("Data scraped successfully and saved.")
            print("Processing complete. Check the generated files.")

    write_excel('kritikos_7k_products.xlsx')

scrape(url_category)