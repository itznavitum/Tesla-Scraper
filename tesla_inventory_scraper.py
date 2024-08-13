# Import necessary libraries
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def configurables():
    """
    Reads and loads configuration data from a file named 'configurables.txt'.

    Returns:
        dict: Configuration data loaded from the file.
    """
    with open('configurables.txt','r') as f:
        data = f.read()

    # Parse the JSON data into a dictionary
    configurables_data = json.loads(data)
    return configurables_data

def format_vehicle_info(vehicle_list):
    """
    Formats a list of vehicle details into a readable string format.

    Args:
        vehicle_list (list): List of vehicle details.

    Returns:
        str: Formatted string of vehicle details.
    """
    formatted_str = ""
    for vehicle in vehicle_list:
        formatted_str += "Vehicle Details:\n"
        for detail in vehicle:
            formatted_str += f"  - {detail}\n"
        formatted_str += "\n"  # Add a newline between vehicles

    return formatted_str

def send_email(subject, body, from_email, from_password, to_email):
    """
    Sends an email with the specified subject and body.

    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.
        from_email (str): Sender's email address.
        from_password (str): Sender's email password.
        to_email (str): Recipient's email address.
    """
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()  # Start TLS for security

            # Authentication
            s.login(from_email, from_password)

            # Send the email
            s.sendmail(from_email, to_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Load configuration data
    config_data = configurables()

    driver = None
    try:
        # Set up Chrome options
        options = Options()

        # Set up the ChromeDriver service
        service = Service(ChromeDriverManager().install())

        # Initialize WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the web page specified in the configuration
        url = config_data["URL"]
        driver.get(url)

        # Wait for elements to load and interact with them
        elems = driver.find_elements(By.CLASS_NAME, 'tds-form-input-text')
        if elems:
            elem = elems[0]  # Select the first element found

            # Perform actions on the selected element
            elem.send_keys(Keys.BACK_SPACE)  # Clear existing content

            # Type each digit of the ZIP code using NUMPAD keys
            for digit in config_data["Zip Code"]:
                key_to_press = getattr(Keys, f"NUMPAD{digit}")
                elem.send_keys(key_to_press)
                time.sleep(0.1)

            elem.send_keys(Keys.ENTER)
        else:
            print("No elements found with the specified class name.")

        # Wait for the page to load necessary content
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'result-photos-main'))
        )

        time.sleep(int(config_data["Load Time"]))  # Wait for a fixed time to ensure all content loads

        # Extract relevant elements from the page
        cars = driver.find_elements(By.CLASS_NAME, 'result-header')
        features_section = driver.find_elements(By.CLASS_NAME, 'result-features.features-grid')

        # Save extracted data to a file
        with open("cars.txt", "w", encoding="utf-8") as cars_file:
            count = 0
            for car in cars:
                car_html = car.get_attribute('outerHTML')
                cars_file.write(car.text + "\n")

                car_details = features_section[count].text
                cars_file.write(car_details + "\n-------------------------\n")
                count += 1


    except Exception as e:
        print(f'Error: {e}')
        raise

    finally:
        # Ensure the browser is closed
        if driver:
            driver.quit()
        print('done')

    # Process the saved car details
    with open("cars.txt", "r") as fh:
        car_list = fh.read().split("-------------------------")

    cars_found = []
    for car in car_list:
        max_price = int(config_data["Max Price - Autopilot"])
        car_details = car.strip().split("\n")
        car_model = car_details[0]
        print(car_model)

        # Check if car model matches the required years
        correct_year = any(year in car_model for year in config_data["Model Years"])
        if not correct_year:
            continue

        # Adjust max price if the car has Full Self-Driving Capability
        if 'Full Self-Driving Capability' in car_details:
            max_price = int(config_data["Max Price - Full Self-Driving Capability"])

        car_transport_fee = 0
        for detail in car_details:
            if "No Est. Transport Fee" in detail:
                car_transport_fee = 0
            elif "Est. Transport Fee:" in detail:
                car_transport_fee = int(detail.split("$")[-1].replace(",", ""))
                print(car_transport_fee)
            elif re.search(r"^\$\d+,\d+$", detail):
                car_price = int(detail.split("$")[-1].replace(",", ""))
                print(car_price)

        overall_car_price = car_price + car_transport_fee
        print("Max Price", max_price)
        if overall_car_price <= max_price:
            print("FOUND")
            cars_found.append(car_details)

    print(cars_found)

    # Send email notification if cars are found
    if cars_found:
        cars_found_set = []
        [cars_found_set.append(x) for x in cars_found if x not in cars_found_set]

        subject = "Cars Found"
        body = str(config_data["URL"]) + "\n\nHere is the list of cars found:\n\n" + format_vehicle_info(cars_found_set)
        from_email = config_data["From Email, Password"]["Email"]
        from_password = config_data["From Email, Password"]["Password"]
        to_email = config_data["Email Ids"]

        for email in to_email:
            send_email(subject, body, from_email, from_password, email)
    else:
        print("No Cars Found")


if __name__ == '__main__':
    main()
