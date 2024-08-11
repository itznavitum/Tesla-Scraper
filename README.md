# Tesla Inventory Scraper and Email Notifier

This Python project automates the process of scraping Tesla's official inventory website to find vehicles matching specific criteria. It sends an email notification with the details of matching vehicles.

## Features

- **Web Scraping**: Automatically navigates Tesla's inventory website and extracts vehicle information.
- **Data Processing**: Filters vehicles based on criteria such as model year, price, and features (e.g., Autopilot, Full Self-Driving Capability).
- **Email Notifications**: Sends an email alert with details of matching vehicles.
- **Configuration File**: Uses a `configurables.txt` file for easy customization of search parameters, such as URL, ZIP code, price limits, and email details.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- pip for package management

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## Configuration

### Configure the Script

Create and update the `configurables.txt` file with your desired settings.
This file should be in JSON format and should include details such as the Tesla inventory URL, ZIP code, model years, price limits, and email credentials.

### Detailed Configuration Breakdown

- **Zip Code**: The ZIP code that the Tesla website uses to determine the availability of vehicles. This should be set to the ZIP code you want to search within.

- **URL**: The URL of Tesla's inventory page with your desired filters applied. Visit the Tesla inventory website, apply all your desired filters (such as interior color, seating configuration, year, etc.), and then copy the URL into this field. This ensures the script scrapes the exact results you are interested in.

- **Model Years**: A list of model years you are interested in. The script will only consider vehicles from the specified years.

- **Max Price - Full Self-Driving Capability**: The maximum price you are willing to pay for a vehicle that includes Tesla’s Full Self-Driving Capability. Vehicles exceeding this price will be excluded from the results.

- **Max Price - Autopilot**: The maximum price you are willing to pay for a vehicle with basic Autopilot but without Full Self-Driving Capability. Vehicles exceeding this price will be excluded from the results.

- **Load Time**: The time in seconds that the script should wait for the page to fully load before extracting vehicle information. Increase this if your internet connection is slow or the page takes longer to load.

- **From Email, Password**: Your email credentials. This is the email address and password used to send notifications. The script uses Gmail's SMTP server to send out emails.

- **Email Ids**: A list of email addresses that will receive notifications if matching vehicles are found.

## Tesla Inventory Specifics

This script is tailored to work with Tesla's inventory pages. You can adjust the URL in the `configurables.txt` file to target specific models (e.g., Model 3, Model S).

## Usage

### Run the Script

Execute the script using Python:

```bash
python tesla_inventory_scraper.py
```
or
```bash
py tesla_inventory_scraper.py
```
  
## Usage

### What the Script Does

The script will:

- **Open a Chrome browser.**
- **Navigate to the specified Tesla inventory URL.**
- **Search for vehicles** based on the criteria in the `configurables.txt` file (e.g., specific model years, price, features).
- **Extract vehicle details** and save them in `cars.txt`.

### Email Notification

If any vehicles match the criteria, an email will be sent to the recipients listed in the `configurables.txt` file, containing the details of the found vehicles.

## Output

- **`cars.txt`:** Contains details of the vehicles found.

## Troubleshooting

### Driver Issues

Ensure you have the latest version of Chrome installed. The script manages ChromeDriver using `webdriver-manager`.

## Contribution

Contributions are welcome! Feel free to fork this project, submit issues, or create pull requests.
