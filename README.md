# kritikos-store-products-scraper
This script uses python-selenium to scrape all of the products from kritikos store. As result it creates an excel file.

This project is designed to scrape product information from the Kritikos Supermarket website using Python and Selenium. It includes two main scripts:

- kritikos_scraper.py - Scrapes all products across multiple categories.
- kritikos_enhance.py - Enhances the scraped data by adding more detailed product information.

# Project Overview
The project aims to scrape product details from the Kritikos Supermarket website. It extracts information such as product names, prices, categories, and images. Additionally, the project enhances the data by including product descriptions and unique key codes.

# Features
- Scrapes product details from multiple categories.
- Scrolls through dynamically loading pages to capture all products.
- Exports scraped data to an Excel file.
- Enhances the scraped data by adding key codes and descriptions.

# Prerequisites
Before running the scripts, ensure you have the following installed:

- Selenium
- Pandas
- tqdm
- Undetected Chromedriver
- Chrome WebDriver

# Usage

# 1. Running kritikos_scraper.py

This script scrapes product information from the Kritikos Supermarket website.

Open the terminal and navigate to the project directory.

# Run the script:
- python kritikos_scraper.py

# The script will:
- Access the specified categories.
- Scroll through the pages to load all products.
- Extract product titles, prices, images, and URLs.
- Save the data in an Excel file named kritikos_7k_products.xlsx.

# 2. Running kritikos_enhance.py
This script enhances the previously scraped data by adding more detailed product information.

Ensure that kritikos_7k_products.xlsx is in the project directory.

# Run the script:
- python kritikos_enhance.py

# The script will:
- Load the Excel file.
- Visit each product's page to scrape additional details like the Key Code and Description.
- Update the Excel file with this new information.

# Output
kritikos_7k_products.xlsx: The initial Excel file containing the scraped product data.
kritikos_7k_update.xlsx: The enhanced Excel file with additional product details.
