import os
import time
import logging
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sub_agents.scraper_agent.scraper_tool import scrape_linkedin_profile

# --- CONFIGURATION ---
# Google Sheet info
SHEET_ID = '1eH_Ebq83ZBZ3GS6XcV4BX2YsjfvW5C74D5_GSuYzrQA'  # Recruiters sheet
SHEET_TAB = 'Sheet1'
LINKEDIN_COL = 'LinkedIn Profile'
EMAIL_COL = 'Email Address'
PHONE_COL = 'Phone Number'

# Path to your Google service account credentials JSON
GOOGLE_CREDS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'client.json')

# --- LOAD ENVIRONMENT ---
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# --- SETUP GOOGLE SHEETS CLIENT ---
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS, scope)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.worksheet(SHEET_TAB)

# --- GET ALL ROWS ---
rows = worksheet.get_all_records()
headers = worksheet.row_values(1)

# Find column indices
linkedin_idx = headers.index(LINKEDIN_COL)
email_idx = headers.index(EMAIL_COL)
phone_idx = headers.index(PHONE_COL)

# --- SCRAPE AND UPDATE ---
for i, row in enumerate(rows, start=2):  # start=2 because row 1 is headers
    profile_url = row.get(LINKEDIN_COL, '').strip()
    if not profile_url or not profile_url.startswith('http'):
        continue
    print(f"Scraping ({i}): {profile_url}")
    result = scrape_linkedin_profile(profile_url)
    if result['status'] == 'success':
        profile = result['profile']
        email = profile.get('email', '')
        phone = profile.get('phone', '')
        # Only update if new info is found
        updates = []
        if email and not row.get(EMAIL_COL):
            worksheet.update_cell(i, email_idx + 1, email)
            updates.append('email')
        if phone and not row.get(PHONE_COL):
            worksheet.update_cell(i, phone_idx + 1, phone)
            updates.append('phone')
        print(f"  → Updated: {', '.join(updates) if updates else 'No new info'}")
    else:
        print(f"  → Error: {result['message']}")
    time.sleep(5)  # Delay to avoid being blocked by LinkedIn

print("Done scraping all recruiter profiles!")
