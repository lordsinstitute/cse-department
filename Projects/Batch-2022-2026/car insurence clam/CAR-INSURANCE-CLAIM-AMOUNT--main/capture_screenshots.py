#!/usr/bin/env python3
"""Capture screenshots of C11 Car Insurance Claim Prediction app using Selenium."""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://127.0.0.1:5002"
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
    # ------------------------------------------------------------------ #
    # 1. Login page (GET /login)
    # ------------------------------------------------------------------ #
    print("[1/14] Login page")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    time.sleep(1)
    save("login.png")

    # ------------------------------------------------------------------ #
    # 2. Registration page (GET /register)
    # ------------------------------------------------------------------ #
    print("[2/14] Registration page")
    driver.get(f"{BASE}/register")
    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    time.sleep(1)
    save("register.png")

    # ------------------------------------------------------------------ #
    # 3. Invalid login attempt (wrong credentials)
    # ------------------------------------------------------------------ #
    print("[3/14] Invalid login attempt")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    save("invalid_login.png")

    # ------------------------------------------------------------------ #
    # 4. Duplicate registration (username "admin" already exists)
    # ------------------------------------------------------------------ #
    print("[4/14] Duplicate registration attempt")
    driver.get(f"{BASE}/register")
    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys("Test Admin")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("testpass123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    save("duplicate_register.png")

    # ------------------------------------------------------------------ #
    # 5. Login as admin (admin / admin123)
    # ------------------------------------------------------------------ #
    print("[5/14] Logging in as admin...")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    # ------------------------------------------------------------------ #
    # 6. Home / dashboard overview (GET /home)
    # ------------------------------------------------------------------ #
    print("[6/14] Home page")
    wait.until(EC.url_contains("/home"))
    time.sleep(1)
    save("home.png")

    # ------------------------------------------------------------------ #
    # 7. Empty prediction form (GET /predict)
    # ------------------------------------------------------------------ #
    print("[7/14] Prediction form (empty)")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.NAME, "AGE")))
    time.sleep(1)
    save("predict_form.png")

    # ------------------------------------------------------------------ #
    # 8. Prediction form filled with sample data
    # ------------------------------------------------------------------ #
    print("[8/14] Prediction form (filled)")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.NAME, "AGE")))
    time.sleep(0.5)

    # -- Select dropdowns (categorical options) --
    Select(driver.find_element(By.NAME, "AGE")).select_by_value("26-39")
    Select(driver.find_element(By.NAME, "GENDER")).select_by_value("male")
    Select(driver.find_element(By.NAME, "RACE")).select_by_value("majority")
    Select(driver.find_element(By.NAME, "DRIVING_EXPERIENCE")).select_by_value("10-19y")
    Select(driver.find_element(By.NAME, "EDUCATION")).select_by_value("university")
    Select(driver.find_element(By.NAME, "INCOME")).select_by_value("middle class")
    Select(driver.find_element(By.NAME, "VEHICLE_YEAR")).select_by_value("after 2015")
    Select(driver.find_element(By.NAME, "VEHICLE_TYPE")).select_by_value("sedan")

    # -- Select dropdowns (binary Yes/No: value="0" or "1") --
    Select(driver.find_element(By.NAME, "VEHICLE_OWNERSHIP")).select_by_value("1")
    Select(driver.find_element(By.NAME, "MARRIED")).select_by_value("1")
    Select(driver.find_element(By.NAME, "CHILDREN")).select_by_value("0")

    # -- Select dropdown (postal code) --
    Select(driver.find_element(By.NAME, "POSTAL_CODE")).select_by_value("10065")

    # -- Numeric inputs --
    credit = driver.find_element(By.NAME, "CREDIT_SCORE")
    credit.clear()
    credit.send_keys("0.75")

    mileage = driver.find_element(By.NAME, "ANNUAL_MILEAGE")
    mileage.clear()
    mileage.send_keys("15000")

    violations = driver.find_element(By.NAME, "SPEEDING_VIOLATIONS")
    violations.clear()
    violations.send_keys("0")

    duis = driver.find_element(By.NAME, "DUIS")
    duis.clear()
    duis.send_keys("0")

    accidents = driver.find_element(By.NAME, "PAST_ACCIDENTS")
    accidents.clear()
    accidents.send_keys("1")

    time.sleep(1)
    save("predict_filled.png")

    # ------------------------------------------------------------------ #
    # 9. Submit prediction and capture result
    # ------------------------------------------------------------------ #
    print("[9/14] Prediction result")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", submit_btn)
    wait.until(EC.presence_of_element_located((By.NAME, "AGE")))
    time.sleep(1)
    save("predict_result.png")

    # ------------------------------------------------------------------ #
    # 10. Prediction history (GET /history)
    # ------------------------------------------------------------------ #
    print("[10/14] Prediction history")
    driver.get(f"{BASE}/history")
    time.sleep(1)
    save("history.png")

    # ------------------------------------------------------------------ #
    # 11. EDA visualizations gallery (GET /visualize)
    # ------------------------------------------------------------------ #
    print("[11/14] Visualizations gallery")
    driver.get(f"{BASE}/visualize")
    time.sleep(1)
    save("visualize.png")

    # ------------------------------------------------------------------ #
    # 12. Analytics dashboard - top section (GET /dashboard)
    # ------------------------------------------------------------------ #
    print("[12/14] Analytics dashboard (top)")
    driver.get(f"{BASE}/dashboard")
    time.sleep(1)
    save("dashboard.png")

    # ------------------------------------------------------------------ #
    # 13. Analytics dashboard - scrolled down for charts
    # ------------------------------------------------------------------ #
    print("[13/14] Analytics dashboard (charts)")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    save("dashboard_charts.png")

    # ------------------------------------------------------------------ #
    # 14. About page (GET /about)
    # ------------------------------------------------------------------ #
    print("[14/14] About page")
    driver.get(f"{BASE}/about")
    time.sleep(1)
    save("about.png")

    print(f"\nAll 14 screenshots saved to: {SAVE_DIR}")

finally:
    driver.quit()
