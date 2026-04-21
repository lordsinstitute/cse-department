#!/usr/bin/env python3
"""Capture screenshots of B21 MindfulPath app using Selenium."""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://127.0.0.1:5006"
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
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


def login(email, password):
    driver.get(f"{BASE}/login")
    time.sleep(0.5)
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
    ).click()
    time.sleep(1)


def logout():
    driver.get(f"{BASE}/logout")
    time.sleep(0.5)


try:
    # ── 1. Login page ────────────────────────────────────────────────
    print("1/14  Login page")
    driver.get(f"{BASE}/login")
    time.sleep(1)
    save("login.png")

    # ── 2. Register page ─────────────────────────────────────────────
    print("2/14  Register page")
    driver.get(f"{BASE}/register")
    time.sleep(1)
    save("register.png")

    # ── 3. Invalid login ─────────────────────────────────────────────
    print("3/14  Invalid login")
    login("wrong@example.com", "wrongpassword")
    time.sleep(0.5)
    save("invalid_login.png")

    # ── 4. Duplicate registration ─────────────────────────────────────
    print("4/14  Duplicate registration")
    driver.get(f"{BASE}/register")
    time.sleep(0.5)
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys("Admin User")
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys("admin@mindfulpath.com")
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys("admin123")
    from selenium.webdriver.support.ui import Select

    Select(driver.find_element(By.NAME, "role")).select_by_value("user")
    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
    ).click()
    time.sleep(1)
    save("duplicate_register.png")

    # ── 5. User dashboard ─────────────────────────────────────────────
    print("5/14  User dashboard")
    login("patient@mindfulpath.com", "patient123")
    driver.get(f"{BASE}/dashboard")
    time.sleep(1)
    save("user_dashboard.png")

    # ── 6. Chat page ──────────────────────────────────────────────────
    print("6/14  Chat page")
    driver.get(f"{BASE}/chat")
    time.sleep(1)
    save("chat.png")

    # ── 7. Chat conversation ──────────────────────────────────────────
    print("7/14  Chat conversation")
    # Click new chat button
    try:
        new_chat_btn = driver.find_element(By.ID, "newChatBtn")
        driver.execute_script("arguments[0].click();", new_chat_btn)
        time.sleep(2)
    except Exception:
        try:
            new_chat_btn = driver.find_element(
                By.CSS_SELECTOR,
                "button.btn-accent, .new-chat-btn, [onclick*='newChat']",
            )
            driver.execute_script("arguments[0].click();", new_chat_btn)
            time.sleep(2)
        except Exception:
            pass

    # Type message
    chat_input = driver.find_element(By.ID, "chatInput")
    chat_input.send_keys(
        "I've been feeling anxious lately and could use some support"
    )
    time.sleep(0.5)

    # Send
    send_btn = driver.find_element(By.ID, "sendBtn")
    driver.execute_script("arguments[0].click();", send_btn)
    time.sleep(3)
    save("chat_conversation.png")

    # ── 8. Mood tracker ───────────────────────────────────────────────
    print("8/14  Mood tracker")
    driver.get(f"{BASE}/mood")
    time.sleep(1)
    save("mood_tracker.png")

    # ── 9. Log a mood entry ───────────────────────────────────────────
    print("9/14  Log a mood entry")
    # Select mood_score radio button with value "4" (happy)
    mood_radio = driver.find_element(
        By.CSS_SELECTOR, "input[name='mood_score'][value='4']"
    )
    driver.execute_script("arguments[0].click();", mood_radio)
    time.sleep(0.3)

    # Fill journal text
    journal = driver.find_element(By.NAME, "journal_text")
    journal.clear()
    journal.send_keys("Feeling good today after meditation")
    time.sleep(0.3)

    # Submit the form
    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
    ).click()
    time.sleep(1)
    save("mood_logged.png")

    # ── 10. Meditations ───────────────────────────────────────────────
    print("10/14  Meditations")
    driver.get(f"{BASE}/meditations")
    time.sleep(1)
    save("meditations.png")

    # ── 11. Therapists ────────────────────────────────────────────────
    print("11/14  Therapists")
    driver.get(f"{BASE}/therapists")
    time.sleep(1)
    save("therapists.png")

    # ── 12. Sessions ──────────────────────────────────────────────────
    print("12/14  Sessions")
    driver.get(f"{BASE}/sessions")
    time.sleep(1)
    save("sessions.png")

    # ── 13. About ─────────────────────────────────────────────────────
    print("13/14  About")
    driver.get(f"{BASE}/about")
    time.sleep(1)
    save("about.png")

    # ── 14. Admin dashboard ───────────────────────────────────────────
    print("14/14  Admin dashboard")
    logout()
    login("admin@mindfulpath.com", "admin123")
    driver.get(f"{BASE}/dashboard")
    time.sleep(1)
    save("admin_dashboard.png")

    print("\nAll 14 screenshots captured successfully!")

finally:
    driver.quit()
