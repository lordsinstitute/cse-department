#!/usr/bin/env python3
"""Capture screenshots of B6 Medical Blockchain app using Selenium."""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://127.0.0.1:5005"
SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
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


def login(username, password):
    """Navigate to login page and log in with given credentials."""
    driver.get(f"{BASE}/login")
    time.sleep(1)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)


def logout():
    """Log out by navigating to /logout."""
    driver.get(f"{BASE}/logout")
    time.sleep(1)


try:
    # ───────────────────────────────────────────────
    # 1. Login page
    # ───────────────────────────────────────────────
    print("[1/14] Login page")
    driver.get(f"{BASE}/login")
    time.sleep(1)
    save("login.png")

    # ───────────────────────────────────────────────
    # 2. Register page
    # ───────────────────────────────────────────────
    print("[2/14] Register page")
    driver.get(f"{BASE}/register")
    time.sleep(1)
    save("register.png")

    # ───────────────────────────────────────────────
    # 3. Invalid login — wrong credentials
    # ───────────────────────────────────────────────
    print("[3/14] Invalid login")
    driver.get(f"{BASE}/login")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    save("invalid_login.png")

    # ───────────────────────────────────────────────
    # 4. Duplicate registration — try registering "admin"
    # ───────────────────────────────────────────────
    print("[4/14] Duplicate registration")
    driver.get(f"{BASE}/register")
    time.sleep(1)
    driver.find_element(By.NAME, "name").send_keys("Admin User")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)
    save("duplicate_register.png")

    # ───────────────────────────────────────────────
    # 5. Admin dashboard — login as admin, go to /home
    # ───────────────────────────────────────────────
    print("[5/14] Admin dashboard")
    login("admin", "admin123")
    driver.get(f"{BASE}/home")
    time.sleep(1)
    save("admin_dashboard.png")

    # ───────────────────────────────────────────────
    # 6. Admin audit trail — /audit
    # ───────────────────────────────────────────────
    print("[6/14] Audit trail")
    driver.get(f"{BASE}/audit")
    time.sleep(1)
    save("audit_trail.png")

    # ───────────────────────────────────────────────
    # 7. Blockchain explorer — /blockchain
    # ───────────────────────────────────────────────
    print("[7/14] Blockchain explorer")
    driver.get(f"{BASE}/blockchain")
    time.sleep(1)
    save("blockchain_explorer.png")

    # ───────────────────────────────────────────────
    # 8. Verify blockchain — /verify
    # ───────────────────────────────────────────────
    print("[8/14] Blockchain verify")
    driver.get(f"{BASE}/verify")
    time.sleep(1)
    save("blockchain_verify.png")

    # ───────────────────────────────────────────────
    # 9. Dashboard with charts — /dashboard
    # ───────────────────────────────────────────────
    print("[9/14] Dashboard with charts")
    driver.get(f"{BASE}/dashboard")
    time.sleep(2)  # extra time for Chart.js to render
    save("dashboard.png")

    # ───────────────────────────────────────────────
    # 10. Upload report — login as doctor, go to /upload
    # ───────────────────────────────────────────────
    print("[10/14] Upload report (doctor)")
    logout()
    login("dr_ahmed", "doctor123")
    driver.get(f"{BASE}/upload")
    time.sleep(1)
    save("upload_report.png")

    # ───────────────────────────────────────────────
    # 11. Doctor's patient reports — /patient-reports
    # ───────────────────────────────────────────────
    print("[11/14] Doctor patient reports")
    driver.get(f"{BASE}/patient-reports")
    time.sleep(1)
    save("doctor_reports.png")

    # ───────────────────────────────────────────────
    # 12. My reports — login as patient, go to /my-reports
    # ───────────────────────────────────────────────
    print("[12/14] My reports (patient)")
    logout()
    login("patient1", "patient123")
    driver.get(f"{BASE}/my-reports")
    time.sleep(1)
    save("my_reports.png")

    # ───────────────────────────────────────────────
    # 13. About page — /about
    # ───────────────────────────────────────────────
    print("[13/14] About page")
    driver.get(f"{BASE}/about")
    time.sleep(1)
    save("about.png")

    # ───────────────────────────────────────────────
    # 14. Share report — /share/1
    # ───────────────────────────────────────────────
    print("[14/14] Share report page")
    driver.get(f"{BASE}/share/1")
    time.sleep(1)
    save("share_report.png")

    print("\nAll 14 screenshots captured successfully!")

finally:
    driver.quit()
    print("Browser closed.")
