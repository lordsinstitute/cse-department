#!/usr/bin/env python3
"""
Capture application screenshots for the B10 DDoS Detection project report.
Starts the Flask app, uses Selenium headless Chrome to capture all pages.
"""
import subprocess
import time
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5021"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "..", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

TEST_USER = {"name": "Test User", "username": "testscreenshot", "password": "test1234"}

# DDoS sample data (high byte/packet counts → likely DDoS)
DDOS_DATA = {
    "switch": "3", "pktcount": "45000", "bytecount": "4500000",
    "dur": "2", "dur_nsec": "500000000", "flows": "350",
    "pktrate": "4500.0", "Pairflow": "200", "port_no": "80",
    "tx_bytes": "4000000", "rx_bytes": "4200000",
    "tx_kbps": "9500.0", "rx_kbps": "9800.0",
}

# Normal sample data (low/moderate values → likely Normal)
NORMAL_DATA = {
    "switch": "1", "pktcount": "150", "bytecount": "5000",
    "dur": "60", "dur_nsec": "100000000", "flows": "5",
    "pktrate": "2.5", "Pairflow": "3", "port_no": "443",
    "tx_bytes": "3000", "rx_bytes": "2500",
    "tx_kbps": "1.5", "rx_kbps": "1.2",
}


def wait_for_server(url, timeout=60):
    """Wait for the Flask server to be ready."""
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url + "/login", timeout=3)
            return True
        except Exception:
            time.sleep(1)
    return False


def take_screenshot(driver, name, wait_time=1):
    """Take a screenshot and save it."""
    time.sleep(wait_time)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"  Captured: {name}.png")
    return path


def fill_prediction_form(driver, data):
    """Fill the prediction form with given data."""
    fields = ['switch', 'pktcount', 'bytecount', 'dur', 'dur_nsec', 'flows',
              'pktrate', 'Pairflow', 'port_no', 'tx_bytes', 'rx_bytes', 'tx_kbps', 'rx_kbps']
    for field in fields:
        try:
            el = driver.find_element(By.NAME, field)
            el.clear()
            el.send_keys(data[field])
        except Exception:
            pass


def main():
    # Start Flask app in background
    print("Starting Flask app on port 5021...")
    flask_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=SCRIPT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_server(BASE_URL):
            print("ERROR: Flask app did not start within 60 seconds")
            flask_proc.kill()
            sys.exit(1)
        print("Flask app is running.")

        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--force-device-scale-factor=1")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)

        print("\nCapturing screenshots...")

        # 1. Home page
        driver.get(f"{BASE_URL}/")
        take_screenshot(driver, "home", wait_time=2)

        # 2. Login page
        driver.get(f"{BASE_URL}/login")
        take_screenshot(driver, "login")

        # 3. Registration page
        driver.get(f"{BASE_URL}/register")
        take_screenshot(driver, "register")

        # 4. Register a test user
        try:
            driver.find_element(By.NAME, "name").send_keys(TEST_USER["name"])
            driver.find_element(By.NAME, "username").send_keys(TEST_USER["username"])
            driver.find_element(By.NAME, "password").send_keys(TEST_USER["password"])
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            time.sleep(1)
        except Exception as e:
            print(f"  Registration may have failed (user might exist): {e}")

        # 5. Login with test user
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys(TEST_USER["username"])
        driver.find_element(By.NAME, "password").send_keys(TEST_USER["password"])
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        time.sleep(2)

        # 6. Prediction page (empty form)
        driver.get(f"{BASE_URL}/predict")
        take_screenshot(driver, "prediction")

        # 7. Prediction - DDoS result
        try:
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            fill_prediction_form(driver, DDOS_DATA)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            take_screenshot(driver, "prediction_ddos", wait_time=2)
        except Exception as e:
            print(f"  DDoS prediction may have failed: {e}")
            take_screenshot(driver, "prediction_ddos")

        # 8. Prediction - Normal result
        try:
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            fill_prediction_form(driver, NORMAL_DATA)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            take_screenshot(driver, "prediction_normal", wait_time=2)
        except Exception as e:
            print(f"  Normal prediction may have failed: {e}")
            take_screenshot(driver, "prediction_normal")

        # 9. Suggestion page (after DDoS prediction)
        try:
            # Make a DDoS prediction first so suggestions show DDoS tips
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            fill_prediction_form(driver, DDOS_DATA)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            time.sleep(1)
            driver.get(f"{BASE_URL}/suggestion")
            take_screenshot(driver, "suggestion_ddos", wait_time=2)
        except Exception as e:
            print(f"  DDoS suggestion may have failed: {e}")
            take_screenshot(driver, "suggestion_ddos")

        # 10. Suggestion page (after Normal prediction)
        try:
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            fill_prediction_form(driver, NORMAL_DATA)
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            time.sleep(1)
            driver.get(f"{BASE_URL}/suggestion")
            take_screenshot(driver, "suggestion_normal", wait_time=2)
        except Exception as e:
            print(f"  Normal suggestion may have failed: {e}")
            take_screenshot(driver, "suggestion_normal")

        # 11. Dashboard page
        driver.get(f"{BASE_URL}/dashboard")
        take_screenshot(driver, "dashboard", wait_time=3)

        # 12. Simulate some traffic on dashboard
        try:
            count_input = driver.find_element(By.NAME, "count")
            count_input.clear()
            count_input.send_keys("10")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            take_screenshot(driver, "simulation", wait_time=3)
        except Exception as e:
            print(f"  Simulation may have failed: {e}")
            take_screenshot(driver, "simulation")

        # 13. Model Info page
        driver.get(f"{BASE_URL}/model-info")
        take_screenshot(driver, "model_info", wait_time=2)

        # 14. Invalid login credentials
        driver.get(f"{BASE_URL}/logout")
        time.sleep(1)
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        take_screenshot(driver, "invalid_login", wait_time=2)

        # 15. Duplicate username registration
        driver.get(f"{BASE_URL}/register")
        time.sleep(1)
        driver.find_element(By.NAME, "name").send_keys("Duplicate User")
        driver.find_element(By.NAME, "username").send_keys(TEST_USER["username"])
        driver.find_element(By.NAME, "password").send_keys("somepass123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        take_screenshot(driver, "duplicate_register", wait_time=2)

        driver.quit()
        print(f"\nAll screenshots saved to: {SCREENSHOT_DIR}/")

    finally:
        print("Stopping Flask app...")
        flask_proc.terminate()
        try:
            flask_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            flask_proc.kill()
        print("Done.")


if __name__ == "__main__":
    main()
