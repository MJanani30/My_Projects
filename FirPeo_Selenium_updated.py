from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Initialize the WebDriver (e.g., Chrome)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Optional: Maximize window on startup

# Path to the ChromeDriver executable
service = Service('C:/Users/WELCOME/AppData/Local/Google/Drivers/chromedriver.exe')  # Adjust the path as needed

driver = None

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open the target website
    driver.get("https://www.fitpeo.com/")

    # Wait for the element using WebDriverWait
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    click_element_xpath = "/html/body/div[1]/div/header/div/div[3]/div[6]/a/div"
    next_element = wait.until(EC.element_to_be_clickable((By.XPATH, click_element_xpath)))
    next_element.click()

    # Allow time for the page to load completely
    time.sleep(20)

    # Take a screenshot of the current page before making changes
    driver.save_screenshot(r'C:\Users\WELCOME\Desktop\Screenshots\before_slider_change.png')

    # Locate the slider thumb and the input field
    thumb = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.MuiSlider-thumb')))
    track = driver.find_element(By.CSS_SELECTOR, '.MuiSlider-track')
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')

    # Set the desired slider value and input value
    desired_percentage = 41
    desired_value = int(input("Enter the Patient Counts"))

    # Update the input field value directly
    driver.execute_script("""
        var inputField = arguments[0];
        var newValue = arguments[1];
        inputField.value = newValue;
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
        inputField.dispatchEvent(new Event('change', { bubbles: true }));
    """, input_field, desired_value)

    # Move the slider thumb to the desired position
    driver.execute_script("""
        var thumb = arguments[0];
        var track = arguments[1];
        var percentage = arguments[2];
        thumb.style.left = percentage + '%';
        track.style.width = percentage + '%';
        var event = new Event('change', { bubbles: true });
        thumb.dispatchEvent(event);
    """, thumb, track, desired_percentage)

    # Add the new element below the slider
    driver.execute_script("""
        var newElement = document.createElement('p');
        newElement.className = 'MuiTypography-root MuiTypography-body1 inter css-12bch19';
        newElement.innerText = arguments[0];
        var sliderContainer = document.querySelector('.MuiSlider-root').parentNode;
        sliderContainer.appendChild(newElement);
    """, desired_value)

    # Wait for the slider and input field to update
    WebDriverWait(driver, 100).until(
        EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, 'input[type="number"]'), str(desired_value))
    )

    # Verify the slider's thumb position and input field value
    thumb_position = thumb.get_attribute('style')
    input_value = input_field.get_attribute('value')
    print(f"Slider thumb position: {thumb_position}")
    print(f"Input field value: {input_value}")

    # Take a screenshot of the page after making changes
    driver.save_screenshot(r'C:\Users\WELCOME\Desktop\Screenshots\after_slider_change.png')

    # Wait for the page to load
    time.sleep(10)  # Adjust the sleep time as needed

    # Define the XPath expressions for the <p> tags you want to update
    xpaths = [
        "//div[contains(@class, 'css-19xu03j')]//p[contains(text(), '200')]",
        "//div[contains(@class, 'MuiToolbar-root')]//p[contains(text(), '200')]"
    ]

    # Define the value to change to
    new_value = '820'

    # Initialize ActionChains
    actions = ActionChains(driver)
    time.sleep(2)

    for index, xpath in enumerate(xpaths):
        # Locate the <p> tag
        p_tag = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Scroll to the <p> tag (optional but helps ensure visibility)
        actions.move_to_element(p_tag).perform()

        # Change the value from 200 to new_value
        driver.execute_script("arguments[0].textContent = arguments[1];", p_tag, new_value)

        # Wait after each update to ensure changes are reflected
        time.sleep(5)

        # Capture a screenshot
        screenshot_filename = f"screenshot_after_update_{index + 1}.png"
        driver.save_screenshot(screenshot_filename)
        print(f"Screenshot saved as {screenshot_filename}")

    # Define the list of XPaths for the checkboxes
    xpaths = [
        '/html/body/div[2]/div[1]/div[2]/div[1]/label/span[1]/input',
        '/html/body/div[2]/div[1]/div[2]/div[2]/label/span[1]/input',
        '/html/body/div[2]/div[1]/div[2]/div[3]/label/span[1]/input'
    ]

    # Base path for saving screenshots
    base_path = 'C:\\Users\\WELCOME\\Desktop\\Screenshots\\'

    # Iterate through the list of XPaths
    for i, xpath in enumerate(xpaths, start=1):
        # Wait for the checkbox element to be present
        checkbox = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Click the checkbox
        checkbox.click()

        # Take a screenshot after clicking the checkbox
        screenshot_path = f'{base_path}after_checkbox_click_{i}.png'
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")

    # Optionally, save changes or perform other actions
    # driver.find_element(By.ID, 'save_button').click()  # Example of clicking a save button

finally:
    # Clean up and close the browser
    driver.quit()
