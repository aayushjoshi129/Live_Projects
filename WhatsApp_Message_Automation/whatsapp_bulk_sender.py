"""
WhatsApp Bulk Messaging via WhatsApp Web
---------------------------------------
Features:
- Read contacts from VCF
- Filter contacts by first name (case-insensitive allow list)
- Personalize message using {name}
- Send message only if WhatsApp chat opens
- Capture SENT / NOT_PRESENT status
- Generate Excel report
"""

import time
from datetime import datetime
from urllib.parse import quote

import pandas as pd
import vobject

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import quopri


# =========================
# USER CONFIGURATION
# =========================
VCF_FILE_PATH = "contacts.vcf"

MESSAGE_TEXT = """✨ Happy New Year 2026! ✨
Hi {name}, Wishing you a year filled with good health, success, and new opportunities. May 2026 bring steady growth, positive outcomes, and peace in both your personal and professional life. 🌟🙏
Best wishes for a prosperous year ahead!"""

# 👇 ONLY these first names will receive messages (case-insensitive)
ALLOWED_FIRST_NAMES = ['Headache']

OUTPUT_EXCEL = "whatsapp_report.xlsx"
SEND_DELAY_SECONDS = 5   # keep >=5 to avoid ban


# Normalize allow-list for case-insensitive comparison
ALLOWED_FIRST_NAMES_SET = {name.lower() for name in ALLOWED_FIRST_NAMES}


# =========================
# INTERNAL FUNCTIONS
# =========================

def read_vcf_contacts(vcf_path):
    contacts = []

    # Read file as binary and decode quoted-printable safely
    with open(vcf_path, "rb") as f:
        raw_data = f.read()

    decoded_data = quopri.decodestring(raw_data).decode(
        "utf-8", errors="ignore"
    )

    for vcard in vobject.readComponents(decoded_data):
        try:
            name = vcard.fn.value if hasattr(vcard, "fn") else "Unknown"

            if hasattr(vcard, "tel_list"):
                for tel in vcard.tel_list:
                    number = (
                        tel.value.replace(" ", "")
                                 .replace("-", "")
                                 .replace("+", "")
                    )

                    if number.isdigit():
                        contacts.append({
                            "name": name,
                            "number": number
                        })
                        break  # first valid number only
        except Exception:
            # Skip malformed contact safely
            continue

    return contacts

def init_whatsapp_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://web.whatsapp.com")
    print("\nScan the WhatsApp QR Code in the opened browser.")
    input("After login is complete, press ENTER to continue...\n")
    return driver


def send_whatsapp_message(driver, phone, message, contact_name):
    try:
        personalized_message = message.replace("{name}", contact_name)
        encoded_message = quote(personalized_message)

        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
        driver.get(url)

        wait = WebDriverWait(driver, 30)

        message_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
            )
        )

        message_box.click()
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)
        time.sleep(2)

        return "SENT"

    except Exception:
        return "NOT_PRESENT"


def generate_excel_report(records, output_file):
    df = pd.DataFrame(records)
    df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(output_file, index=False)


# =========================
# MAIN EXECUTION FLOW
# =========================

def main():
    print("Reading VCF contacts...")
    contacts = read_vcf_contacts(VCF_FILE_PATH)
    print(f"Total contacts loaded: {len(contacts)}")

    if not contacts:
        print("No valid contacts found. Exiting.")
        return

    driver = init_whatsapp_driver()
    results = []

    print("Starting message delivery...\n")

    for idx, contact in enumerate(contacts, start=1):

        # Extract first name
        first_name = contact["name"].strip().split()[0]

        # Filter by allow-list (case-insensitive)
        if first_name.lower() not in ALLOWED_FIRST_NAMES_SET:
            continue

        print(f"[{idx}/{len(contacts)}] Sending to {first_name} ({contact['number']})")

        status = send_whatsapp_message(
            driver,
            contact["number"],
            MESSAGE_TEXT,
            first_name
        )

        results.append({
            "contact_name": contact["name"],
            "phone_number": contact["number"],
            "message": MESSAGE_TEXT.replace("{name}", first_name),
            "status": status
        })

        print(f"Status: {status}\n")
        time.sleep(SEND_DELAY_SECONDS)

    print("Generating Excel report...")
    generate_excel_report(results, OUTPUT_EXCEL)

    driver.quit()
    print(f"\nProcess completed successfully.")
    print(f"Report saved as: {OUTPUT_EXCEL}")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()