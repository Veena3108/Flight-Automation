from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

# Function to book a flight ticket
def book_flight(departure, destination, departure_date, return_date, book_return, passenger_email, passenger_mobile,num_adults, num_children, classType, stop , sFare):
    # Initialize WebDriver (change the path to your WebDriver)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to the travel website
    driver.get("https://www.yatra.com/?_ga=2.235531522.240949936.1713765188-1252859938.1712829404")

    try:
        # Fill out the departure and destination fields
        departure_field = driver.find_element(By.ID, "BE_flight_origin_city")
        departure_field.clear()
        departure_field.send_keys(departure)

        # Wait for the origin options to appear and click the first one
        origin_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{departure}')]")))

        # Use ActionChains to move to the element and then click
        ActionChains(driver).move_to_element(origin_option).click().perform()

        destination_field = driver.find_element(By.ID, "BE_flight_arrival_city")
        destination_field.clear()
        destination_field.send_keys(destination)

        # Wait for the destination options to appear and click the first one
        destination_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{destination}')]")))

        # Use ActionChains to move to the element and then click
        ActionChains(driver).move_to_element(destination_option).click().perform()

        # Enter departure date
        departure_date_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BE_flight_origin_date")))
        departure_date_input.click()

        # Wait for datepicker to appear
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, departure_date)))

        departure_date_element = driver.find_element(By.ID, departure_date)
        departure_date_element.click()

        if book_return == "yes":
            return_date_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "BE_flight_arrival_date")))
            return_date_input.click()

            # Wait for datepicker to appear
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, return_date)))

            return_date_element = driver.find_element(By.ID, return_date)
            return_date_element.click()

        traveller = driver.find_element(By.XPATH, "//div[@id='BE_flight_paxInfoBox']")
        traveller.click()
        time.sleep(1)
        while num_adults > 1:
            adult_plus_button = driver.find_element(By.XPATH, "(//span[@class='ddSpinnerPlus'])[1]")
            adult_plus_button.click()
            time.sleep(1)
            num_adults -= 1

        while num_children > 0:
            child_plus_button = driver.find_element(By.XPATH, "(//span[@class='ddSpinnerPlus'])[2]")
            child_plus_button.click()
            time.sleep(1)
            num_children -= 1

        if classType == "premium economy":
            classTypeB = driver.find_element(By.XPATH, "(//span[@class='ddlabel'])[2]")
            classTypeB.click()
        if classType == "business":
            classTypeB = driver.find_element(By.XPATH, "(//span[@class='ddlabel'])[3]")
            classTypeB.click()

        if stop == "non stop":
            sfare = driver.find_element(By.XPATH, "(//div[@class='filter-list'])")
            sfare.click()

        if sFare == "student fare":
            sfare = driver.find_element(By.XPATH, "(//div[@id='specialFareContainer'])")
            sfare.click()

        if sFare == "armed forces":
            sfare = driver.find_element(By.XPATH, "(//div[@id='armedforcesContainer'])")
            sfare.click()

        if sFare == "senior citizen":
            sfare = driver.find_element(By.XPATH, "(//div[@id='seniorcitizenContainer'])")
            sfare.click()

        # Click on the search button using JavaScript
        search_button = driver.find_element(By.ID, "BE_flight_flsearch_btn")
        driver.execute_script("arguments[0].click();", search_button)

        # Wait for the search results to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "search-page")))

        # Wait for flight details element to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='schedule v-aligm-t pr']")))

        if book_return == "yes":
            book_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@autom='booknow']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", book_button)

            # Click on "Book" button using JavaScript
            driver.execute_script("arguments[0].click();", book_button)

            click_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='fs-14 secondary-button button cursor-pointer bold ']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", click_button)

            # Click on "Book" button using JavaScript
            driver.execute_script("arguments[0].click();", click_button)

        # Check if "View fares" button is present
        try:
            view_fares_button = driver.find_element(By.XPATH, "//button[@autom='morefares']")
            view_fares_button.click()
            print("Button pressed: View Fares")

            # Scroll to "Book" button
            book_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@autom='booknow']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", book_button)

            # Click on "Book" button using JavaScript
            driver.execute_script("arguments[0].click();", book_button)
            print("Button pressed: Book")

        except NoSuchElementException:
            # If "View fares" button is not present, click on "Book Now" button
            book_now_button = driver.find_element(By.XPATH, "//button[contains(text(),'Book Now')]")
            book_now_button.click()
            print("Button pressed: Book Now")

        # Wait for the next page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container-fluid")))

        # Now, fill in passenger details
        email_field = driver.find_element(By.ID, "additionalContactEmail")
        email_field.clear()
        email_field.send_keys(passenger_email)

        mobile_field = driver.find_element(By.ID, "additionalContactMobile")
        mobile_field.clear()
        mobile_field.send_keys(passenger_mobile)

        # You can add more code here to fill in other passenger details if required

    finally:
        # Close the browser window
        driver.quit()


# Example usage
book_flight("DEL", "BLR", "01/05/2024", "04/05/2024", "yes", "vinnibhalla288@gmail.com", "1234567890",2,1, "economy","non stop", "armed forces")
