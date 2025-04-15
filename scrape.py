import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def Scrape_website(website):
    print("Launching Chrome browser...")

    chrome_driver_path = "./chromedriver.exe"  # or set up webdriver-manager for auto-handling
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()

    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
