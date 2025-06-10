from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def selenium_scrape_headlines(url: str) -> dict:
    """
    Uses Selenium to fetch a web page, returning its title and all H1 headlines.
    Args:
        url (str): The URL to scrape.
    Returns:
        dict: { 'status': 'success', 'title': ..., 'headlines': [...] } or { 'status': 'error', 'message': ... }
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        title = driver.title
        headlines = [el.text for el in driver.find_elements(By.TAG_NAME, 'h1')]
        driver.quit()
        return {'status': 'success', 'title': title, 'headlines': headlines}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def simple_crawler(start_url: str, max_depth: int = 2, same_domain_only: bool = True) -> dict:
    """
    Crawl web pages starting from start_url up to max_depth, returning unique URLs found.
    Args:
        start_url (str): The starting URL for the crawl.
        max_depth (int): Maximum crawl depth (default: 2).
        same_domain_only (bool): Only crawl links on the same domain (default: True).
    Returns:
        dict: { 'status': 'success', 'urls': [...] } or { 'status': 'error', 'message': ... }
    """
    try:
        visited = set()
        to_visit = [(start_url, 0)]
        base_domain = urlparse(start_url).netloc if same_domain_only else None
        while to_visit:
            url, depth = to_visit.pop(0)
            if url in visited or depth > max_depth:
                continue
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    abs_url = urljoin(url, link['href'])
                    parsed = urlparse(abs_url)
                    if not parsed.scheme.startswith('http'):
                        continue
                    if same_domain_only and parsed.netloc != base_domain:
                        continue
                    if abs_url not in visited:
                        to_visit.append((abs_url, depth + 1))
            except Exception:
                pass  # skip errors, keep crawling
            visited.add(url)
        return {'status': 'success', 'urls': sorted(visited)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

import re

def extract_linkedin_links_from_html(html: str) -> dict:
    """
    Extract unique LinkedIn profile URLs from a block of HTML (e.g., Google search results).
    Args:
        html (str): The HTML content to search.
    Returns:
        dict: { 'status': 'success', 'linkedin_urls': [...] } or { 'status': 'error', 'message': ... }
    """
    try:
        # Regex for LinkedIn profile URLs (public profiles)
        pattern = r"https?://[\w.]*linkedin\.com/in/[a-zA-Z0-9\-_%]+"
        urls = set(re.findall(pattern, html))
        return {'status': 'success', 'linkedin_urls': sorted(urls)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def scrape_linkedin_profile(url: str) -> dict:
    """
    Uses Selenium to extract recruiter contact info from a LinkedIn profile page.
    Logs into LinkedIn using credentials from .env, uses explicit waits, and handles errors robustly.
    Args:
        url (str): The LinkedIn profile URL.
    Returns:
        dict: { 'status': 'success', 'profile': {...} } or { 'status': 'error', 'message': ... }
    """
    import os
    import logging
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

    options = Options()
    # Allow toggling headless mode via env var for debugging
    if os.getenv('SELENIUM_HEADLESS', '1') != '0':
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # User-Agent spoofing
    user_agent = os.getenv('SELENIUM_USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
    options.add_argument(f'--user-agent={user_agent}')
    # Optional proxy support
    proxy = os.getenv('SELENIUM_PROXY')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        profile = {'name': '', 'company': '', 'email': '', 'phone': ''}

        # 1. Log into LinkedIn
        driver.get('https://www.linkedin.com/login')
        try:
            username = os.getenv('LINKEDIN_USERNAME')
            password = os.getenv('LINKEDIN_PASSWORD')
            if not username or not password:
                raise Exception('LinkedIn credentials not found in environment variables.')
            wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            # Wait for login to complete (profile icon appears or redirect)
            wait.until(EC.presence_of_element_located((By.ID, 'global-nav-search')))  # Robust selector for post-login
        except TimeoutException:
            driver.quit()
            return {'status': 'error', 'message': 'Login to LinkedIn failed. Check credentials or CAPTCHA.'}

        # 2. Navigate to profile URL
        driver.get(url)
        # Detect CAPTCHA or block
        if 'captcha' in driver.current_url.lower():
            driver.quit()
            return {'status': 'error', 'message': 'Blocked by LinkedIn CAPTCHA. Manual intervention required.'}

        # 3. Extract Name
        try:
            name_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.text-heading-xlarge')))
            profile['name'] = name_elem.text.strip()
        except Exception:
            profile['name'] = ''

        # 4. Extract Company (current position)
        try:
            # This selector may need to be updated based on LinkedIn's DOM
            company_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.text-body-medium.break-words')))
            profile['company'] = company_elem.text.strip()
        except Exception:
            profile['company'] = ''

        # 5. Open Contact Info and extract email/phone
        try:
            contact_button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Contact')))
            contact_button.click()
            # Wait for modal
            contact_popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-modal__content')))
            # Email
            email = ''
            phone = ''
            links = contact_popup.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('mailto:'):
                    email = href.replace('mailto:', '')
                    break
            spans = contact_popup.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                text = span.text
                if re.match(r'^[\d\-+() ]{7,}$', text):
                    phone = text
                    break
            profile['email'] = email
            profile['phone'] = phone
        except Exception:
            profile['email'] = ''
            profile['phone'] = ''

        driver.quit()
        return {'status': 'success', 'profile': profile}
    except Exception as e:
        if driver:
            driver.quit()
        logging.exception('Error scraping LinkedIn profile:')
        return {'status': 'error', 'message': f'Scraping failed: {e}'}
