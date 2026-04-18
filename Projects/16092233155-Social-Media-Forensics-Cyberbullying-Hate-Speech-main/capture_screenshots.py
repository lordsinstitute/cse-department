#!/usr/bin/env python3
"""Capture screenshots of C21 Hate Speech Analysis app using Selenium."""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://127.0.0.1:5007"
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
    # ------------------------------------------------------------------ 1
    print("[1/14] Login page")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    time.sleep(1)
    save("login.png")

    # ------------------------------------------------------------------ 2
    print("[2/14] Register page")
    driver.get(f"{BASE}/register")
    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    time.sleep(1)
    save("register.png")

    # ------------------------------------------------------------------ 3
    print("[3/14] Invalid login attempt")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    save("invalid_login.png")

    # ------------------------------------------------------------------ 4
    print("[4/14] Duplicate registration (username 'admin')")
    driver.get(f"{BASE}/register")
    wait.until(EC.presence_of_element_located((By.NAME, "name")))
    driver.find_element(By.NAME, "name").send_keys("Admin User")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("test1234")
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    save("duplicate_register.png")

    # ------------------------------------------------------------------ 5
    print("[5/--] Logging in as admin...")
    driver.get(f"{BASE}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)

    # ------------------------------------------------------------------ 6
    print("[6/14] Home / Dashboard")
    driver.get(f"{BASE}/home")
    time.sleep(1)
    save("home.png")

    # ------------------------------------------------------------------ 7
    print("[7/14] Predict form (empty)")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.ID, "textInput")))
    time.sleep(1)
    save("predict_form.png")

    # ------------------------------------------------------------------ 8
    print("[8/14] Predict — hate speech")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.ID, "textInput")))
    textarea = driver.find_element(By.ID, "textInput")
    textarea.send_keys(
        "I hate those people, they should all be deported and never come back"
    )
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    save("predict_hate.png")

    # ------------------------------------------------------------------ 9
    print("[9/14] Predict — clean text")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.ID, "textInput")))
    textarea = driver.find_element(By.ID, "textInput")
    textarea.send_keys(
        "What a beautiful day! I love spending time with my family in the park"
    )
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    save("predict_clean.png")

    # ------------------------------------------------------------------ 10
    print("[10/14] Predict — offensive text")
    driver.get(f"{BASE}/predict")
    wait.until(EC.presence_of_element_located((By.ID, "textInput")))
    textarea = driver.find_element(By.ID, "textInput")
    textarea.send_keys(
        "That movie was so stupid, the director is an absolute idiot"
    )
    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1)
    save("predict_offensive.png")

    # ------------------------------------------------------------------ 11
    print("[11/14] Prediction history")
    driver.get(f"{BASE}/history")
    time.sleep(1)
    save("history.png")

    # ------------------------------------------------------------------ 12
    print("[12/14] EDA visualizations")
    driver.get(f"{BASE}/visualize")
    time.sleep(1)
    save("visualize.png")

    # ------------------------------------------------------------------ 13
    print("[13/14] Model dashboard")
    driver.get(f"{BASE}/dashboard")
    time.sleep(1)
    save("dashboard.png")

    # ------------------------------------------------------------------ 14
    print("[14/14] About page")
    driver.get(f"{BASE}/about")
    time.sleep(1)
    save("about.png")

    print("\nAll 14 screenshots captured successfully!")

finally:
    driver.quit()
    print("Browser closed.")
