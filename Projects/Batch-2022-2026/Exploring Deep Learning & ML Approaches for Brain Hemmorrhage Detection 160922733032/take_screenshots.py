#!/usr/bin/env python3
"""
Capture application screenshots for the C18 Brain Hemorrhage Detection project report.
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

BASE_URL = "http://127.0.0.1:5010"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "..", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

TEST_USER = {"name": "Test User", "username": "testscreenshot", "password": "test1234"}


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


def main():
    # Start Flask app in background
    print("Starting Flask app on port 5010...")
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

        # 1. Login page
        driver.get(f"{BASE_URL}/login")
        take_screenshot(driver, "login", wait_time=2)

        # 2. Registration page
        driver.get(f"{BASE_URL}/register")
        take_screenshot(driver, "register")

        # 3. Register a test user
        try:
            driver.find_element(By.NAME, "name").send_keys(TEST_USER["name"])
            driver.find_element(By.NAME, "username").send_keys(TEST_USER["username"])
            driver.find_element(By.NAME, "password").send_keys(TEST_USER["password"])
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            time.sleep(1)
        except Exception as e:
            print(f"  Registration may have failed (user might exist): {e}")

        # 4. Login with test user
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys(TEST_USER["username"])
        driver.find_element(By.NAME, "password").send_keys(TEST_USER["password"])
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        time.sleep(2)

        # 5. Home page (logged in)
        driver.get(f"{BASE_URL}/home")
        take_screenshot(driver, "home", wait_time=2)

        # 6. Prediction page (empty form)
        driver.get(f"{BASE_URL}/predict")
        take_screenshot(driver, "predict", wait_time=2)

        # 7. Prediction - Stroke result (upload stroke sample)
        try:
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            # Find a stroke sample image
            samples_dir = os.path.join(SCRIPT_DIR, "static", "test_samples")
            stroke_img = None
            if os.path.exists(samples_dir):
                for f in sorted(os.listdir(samples_dir)):
                    if "stroke" in f.lower():
                        stroke_img = os.path.join(samples_dir, f)
                        break
            if not stroke_img:
                # Try from Dataset
                dataset_stroke = os.path.join(SCRIPT_DIR, "Dataset", "test", "stroke")
                if os.path.exists(dataset_stroke):
                    files = sorted(os.listdir(dataset_stroke))
                    if files:
                        stroke_img = os.path.join(dataset_stroke, files[0])
            if stroke_img:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(stroke_img)
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
                take_screenshot(driver, "predict_stroke", wait_time=3)
            else:
                print("  No stroke sample found, skipping stroke prediction screenshot")
                take_screenshot(driver, "predict_stroke")
        except Exception as e:
            print(f"  Stroke prediction may have failed: {e}")
            take_screenshot(driver, "predict_stroke")

        # 8. Prediction - Normal result (upload normal sample)
        try:
            driver.get(f"{BASE_URL}/predict")
            time.sleep(1)
            normal_img = None
            if os.path.exists(samples_dir):
                for f in sorted(os.listdir(samples_dir)):
                    if "normal" in f.lower():
                        normal_img = os.path.join(samples_dir, f)
                        break
            if not normal_img:
                dataset_normal = os.path.join(SCRIPT_DIR, "Dataset", "test", "normal")
                if os.path.exists(dataset_normal):
                    files = sorted(os.listdir(dataset_normal))
                    if files:
                        normal_img = os.path.join(dataset_normal, files[0])
            if normal_img:
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(normal_img)
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
                take_screenshot(driver, "predict_normal", wait_time=3)
            else:
                print("  No normal sample found, skipping normal prediction screenshot")
                take_screenshot(driver, "predict_normal")
        except Exception as e:
            print(f"  Normal prediction may have failed: {e}")
            take_screenshot(driver, "predict_normal")

        # 9. History page
        driver.get(f"{BASE_URL}/history")
        take_screenshot(driver, "history", wait_time=2)

        # 10. Dashboard page
        driver.get(f"{BASE_URL}/dashboard")
        take_screenshot(driver, "dashboard", wait_time=3)

        # 11. About page
        driver.get(f"{BASE_URL}/about")
        take_screenshot(driver, "about", wait_time=2)

        # 12. Invalid login
        driver.get(f"{BASE_URL}/logout")
        time.sleep(1)
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        driver.find_element(By.NAME, "username").send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        take_screenshot(driver, "invalid_login", wait_time=2)

        # 13. Duplicate registration
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
