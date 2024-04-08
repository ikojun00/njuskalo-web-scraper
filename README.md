# Njuškalo Web Scraper

## Introduction

A web scraper designed to extract apartment listings from Njuškalo along with their details for further analysis or usage.

## How to Use

Follow these steps to utilize the scraper effectively:

### Scraping County Listings for the First Time

1. **Clone Repository**: Start by cloning this repository to your local machine using Git.

    ```bash
    git clone https://github.com/ikojun00/njuskalo-web-scraper.git
    ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies specified in the `requirements.txt` file.

    ```bash
    cd njuskalo-web-scraper
    pip install -r requirements.txt
    ```

3. **Set Configuration**: Open the `apartment_links.py` script located in the `/scripts/` directory. Adjust name of the county (in lowercase) from which you want to extract apartment links.

4. **Run Apartment Links Script**: Execute the `apartment_links.py` script to gather the apartment links based on your configured settings.

    ```bash
    python scripts/apartment_links.py
    ```

5. **Run Apartment Info Script**: After collecting the apartment links, proceed to run the `apartment_info.py` script to extract detailed information about each apartment.

    ```bash
    python scripts/apartment_info.py
    ```

6. **Access Results**: Once the scripts have completed execution, you will find two new files generated: `apartment_links.csv` containing the links and `apartment_info.csv` containing detailed information. You can rename these files according to the county you specified.

### Scraping County Listings That Have Already Been Scraped Before

1. - 4. **Repetition**: Follow steps first four steps from "Scraping County Listings for the First Time".

5. **Run Apartment Diff Script**: After collecting the apartment links, proceed to run the `diff.py` script to remove invalid links from county located in the `/csv/links/` directory. Once the script have completed execution, you will find two new files generated: `new.csv` containing new links and `sold.csv` containing invalid links.

    ```bash
    python scripts/diff.py
    ```
6. **Run Apartment Info Script**: After collecting the new apartment links (`new.csv`), proceed to run the `apartment_info.py` script to extract detailed information about each apartment.

    ```bash
    python scripts/apartment_info.py
    ```

7. **Access Results**: Once the script have completed execution, you will find `apartment_info.csv` containing detailed information. Append rows from `apartment_info.csv` into old file located in the `/csv/info/` directory of county that you wanted to scraped.

## Disclaimer

This scraper is provided for educational purposes only. Use it responsibly and ethically, respecting the terms of service and privacy policies of websites scraped. The developers are not responsible for any misuse or unethical use of this tool.