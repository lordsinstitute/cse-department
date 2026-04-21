#!/usr/bin/env python3
"""Capture screenshots of C6 Carbon Emission Prediction app using Selenium."""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

BASE = "http://127.0.0.1:5012"
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SAVE_DIR, exist_ok=True)

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--force-device-scale-factor=1")
opts.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=opts)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)


def save(name):
    path = os.path.join(SAVE_DIR, name)
    driver.save_screenshot(path)
    print(f"  Saved: {name}")


try:
    # 1. Login page
    print("1. Login Page")
    driver.get(f"{BASE}/login")
    time.sleep(1)
    save("login.png")

    # 2. Registration page
    print("2. Registration Page")
    driver.get(f"{BASE}/register")
    time.sleep(1)
    save("register.png")

    # 3. Invalid login
    print("3. Invalid Login")
    driver.get(f"{BASE}/login")
    time.sleep(0.5)
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
    time.sleep(1)
    save("invalid_login.png")

    # 4. Duplicate registration
    print("4. Duplicate Registration")
    driver.get(f"{BASE}/register")
    time.sleep(0.5)
    driver.find_element(By.NAME, "name").send_keys("Admin User")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
    time.sleep(1)
    save("duplicate_register.png")

    # 5. Access without login
    print("5. Access Without Login")
    driver.delete_all_cookies()
    driver.get(f"{BASE}/home")
    time.sleep(1)
    save("access_without_login.png")

    # 6. Login as admin
    print("6. Logging in as admin...")
    driver.get(f"{BASE}/login")
    time.sleep(0.5)
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
    time.sleep(1)

    # 7. Home page
    print("7. Home Page")
    driver.get(f"{BASE}/home")
    time.sleep(1)
    save("home.png")

    # 8. Predict page (empty form)
    print("8. Predict Page")
    driver.get(f"{BASE}/predict")
    time.sleep(1)
    save("predict.png")

    # 9. Perform prediction
    print("9. Performing CO2 prediction...")
    driver.get(f"{BASE}/predict")
    time.sleep(0.5)

    # Fill in the form
    try:
        Select(driver.find_element(By.NAME, "Make")).select_by_visible_text("Toyota")
    except:
        pass
    try:
        Select(driver.find_element(By.NAME, "Vehicle_Class")).select_by_visible_text("Compact")
    except:
        pass
    try:
        Select(driver.find_element(By.NAME, "Transmission")).select_by_visible_text("Automatic")
    except:
        pass
    try:
        Select(driver.find_element(By.NAME, "Fuel_Type")).select_by_visible_text("Regular Gasoline")
    except:
        pass

    # Numeric fields
    for field_name, value in [("Engine_Size", "2.0"), ("Cylinders", "4"),
                               ("Fuel_Consumption_City", "9.0"),
                               ("Fuel_Consumption_Hwy", "7.0"),
                               ("Fuel_Consumption_Comb", "8.0")]:
        try:
            el = driver.find_element(By.NAME, field_name)
            el.clear()
            el.send_keys(value)
        except:
            pass

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", submit_btn)
    time.sleep(3)

    # 10. Prediction result
    print("10. Prediction Result")
    save("predict_result.png")

    # 11. Scroll down for more details
    print("11. Prediction Result (scrolled)")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    save("predict_result_scroll.png")

    # 12. History page
    print("12. History Page")
    driver.get(f"{BASE}/history")
    time.sleep(1)
    save("history.png")

    # 13. Dashboard
    print("13. Dashboard")
    driver.get(f"{BASE}/dashboard")
    time.sleep(2)
    save("dashboard.png")

    # 14. Dashboard scrolled (more charts)
    print("14. Dashboard (scrolled)")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    save("dashboard_scroll.png")

    # 15. About page
    print("15. About Page")
    driver.get(f"{BASE}/about")
    time.sleep(1)
    save("about.png")

    print("\nAll 15 screenshots captured successfully!")

finally:
    driver.quit()
