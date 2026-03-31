#!/usr/bin/env python3
"""
Capture application screenshots for the B3 Resume Builder project report.
Starts a Python HTTP server, uses Selenium headless Chrome to capture all pages.
"""
import subprocess
import time
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5003"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "..", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

TEST_USER = {"name": "Test User", "username": "testuser", "password": "test1234"}

# Sample resume data to fill in
SAMPLE_DATA = {
    "firstName": "John",
    "lastName": "Doe",
    "title": "Full Stack Developer",
    "email": "john.doe@email.com",
    "phone": "+1 (555) 123-4567",
    "location": "New York, NY",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe",
    "website": "johndoe.dev",
    "summary": "Experienced full stack developer with 5+ years building scalable web applications using React, Node.js, and Python. Led teams of 5+ engineers delivering enterprise SaaS products.",
}


def wait_for_server(url, timeout=30):
    """Wait for the HTTP server to be ready."""
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=3)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def take_screenshot(driver, name, wait_time=1):
    """Take a screenshot and save it."""
    time.sleep(wait_time)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"  Captured: {name}.png")
    return path


def fill_field(driver, field_id, value):
    """Fill a form field by ID."""
    try:
        el = driver.find_element(By.ID, field_id)
        el.clear()
        el.send_keys(value)
    except Exception:
        pass


def main():
    # Start HTTP server in background
    print("Starting HTTP server on port 5003...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "5003"],
        cwd=SCRIPT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_server(BASE_URL):
            print("ERROR: HTTP server did not start within 30 seconds")
            server_proc.kill()
            sys.exit(1)
        print("HTTP server is running.")

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
        driver.get(BASE_URL)
        time.sleep(2)
        take_screenshot(driver, "login")

        # 2. Registration tab
        try:
            driver.execute_script("switchAuthTab('register');")
            time.sleep(1)
            take_screenshot(driver, "register")
        except Exception as e:
            print(f"  Could not switch to register tab: {e}")
            take_screenshot(driver, "register")

        # 3. Register and login
        try:
            driver.find_element(By.ID, "registerName").send_keys(TEST_USER["name"])
            driver.find_element(By.ID, "registerUsername").send_keys(TEST_USER["username"])
            driver.find_element(By.ID, "registerPassword").send_keys(TEST_USER["password"])
            driver.execute_script("registerUser();")
            time.sleep(1)
        except Exception as e:
            print(f"  Registration may have failed: {e}")

        # Try login
        try:
            driver.execute_script("switchAuthTab('login');")
            time.sleep(0.5)
            driver.find_element(By.ID, "loginUsername").send_keys(TEST_USER["username"])
            driver.find_element(By.ID, "loginPassword").send_keys(TEST_USER["password"])
            driver.execute_script("loginUser();")
            time.sleep(2)
        except Exception as e:
            print(f"  Login may have failed: {e}")

        # 4. Personal info section (fill with sample data)
        try:
            # Click Personal section
            driver.execute_script("if(typeof showSection === 'function') showSection('personal');")
            time.sleep(1)

            fill_field(driver, "firstName", SAMPLE_DATA["firstName"])
            fill_field(driver, "lastName", SAMPLE_DATA["lastName"])
            fill_field(driver, "title", SAMPLE_DATA["title"])
            fill_field(driver, "email", SAMPLE_DATA["email"])
            fill_field(driver, "phone", SAMPLE_DATA["phone"])
            fill_field(driver, "location", SAMPLE_DATA["location"])
            fill_field(driver, "linkedin", SAMPLE_DATA["linkedin"])
            fill_field(driver, "github", SAMPLE_DATA["github"])
            fill_field(driver, "website", SAMPLE_DATA["website"])
            fill_field(driver, "summary", SAMPLE_DATA["summary"])

            # Trigger preview update
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(1)
            take_screenshot(driver, "editor_personal")
        except Exception as e:
            print(f"  Personal info fill may have failed: {e}")
            take_screenshot(driver, "editor_personal")

        # 5. Experience section
        try:
            driver.execute_script("if(typeof showSection === 'function') showSection('experience');")
            time.sleep(1)
            # Add an experience entry
            driver.execute_script("if(typeof addExperience === 'function') addExperience();")
            time.sleep(0.5)
            take_screenshot(driver, "editor_experience")
        except Exception as e:
            print(f"  Experience section: {e}")
            take_screenshot(driver, "editor_experience")

        # 6. Education section
        try:
            driver.execute_script("if(typeof showSection === 'function') showSection('education');")
            time.sleep(1)
            driver.execute_script("if(typeof addEducation === 'function') addEducation();")
            time.sleep(0.5)
            take_screenshot(driver, "editor_education")
        except Exception as e:
            print(f"  Education section: {e}")
            take_screenshot(driver, "editor_education")

        # 7. Skills section
        try:
            driver.execute_script("if(typeof showSection === 'function') showSection('skills');")
            time.sleep(1)
            # Add some skills
            for skill in ["JavaScript", "Python", "React", "Node.js", "SQL"]:
                driver.execute_script(f"if(typeof addSkill === 'function') addSkill();")
                time.sleep(0.3)
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(0.5)
            take_screenshot(driver, "editor_skills")
        except Exception as e:
            print(f"  Skills section: {e}")
            take_screenshot(driver, "editor_skills")

        # 8. Professional template (default)
        try:
            driver.execute_script("if(typeof setTemplate === 'function') setTemplate('professional');")
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(1)
            take_screenshot(driver, "resume_professional")
        except Exception as e:
            print(f"  Professional template: {e}")
            take_screenshot(driver, "resume_professional")

        # 9. Modern template
        try:
            driver.execute_script("if(typeof setTemplate === 'function') setTemplate('modern');")
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(1)
            take_screenshot(driver, "resume_modern")
        except Exception as e:
            print(f"  Modern template: {e}")
            take_screenshot(driver, "resume_modern")

        # 10. Creative template
        try:
            driver.execute_script("if(typeof setTemplate === 'function') setTemplate('creative');")
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(1)
            take_screenshot(driver, "resume_creative")
        except Exception as e:
            print(f"  Creative template: {e}")
            take_screenshot(driver, "resume_creative")

        # 11. Executive template
        try:
            driver.execute_script("if(typeof setTemplate === 'function') setTemplate('executive');")
            driver.execute_script("if(typeof updatePreview === 'function') updatePreview();")
            time.sleep(1)
            take_screenshot(driver, "resume_executive")
        except Exception as e:
            print(f"  Executive template: {e}")
            take_screenshot(driver, "resume_executive")

        # 12. ATS score section
        try:
            driver.execute_script("if(typeof setTemplate === 'function') setTemplate('professional');")
            driver.execute_script("if(typeof showSection === 'function') showSection('ats');")
            time.sleep(1)
            driver.execute_script("if(typeof calculateATS === 'function') calculateATS();")
            time.sleep(1)
            take_screenshot(driver, "ats_score")
        except Exception as e:
            print(f"  ATS score: {e}")
            take_screenshot(driver, "ats_score")

        driver.quit()
        print(f"\nAll screenshots saved to: {SCREENSHOT_DIR}/")

    finally:
        print("Stopping HTTP server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
        print("Done.")


if __name__ == "__main__":
    main()
