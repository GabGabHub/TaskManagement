from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_github_issues(limit=10):
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Edge(
        service=Service(r"E:\Gab\Project\msedgedriver.exe"),
        options=edge_options
    )

    tasks = []
    try:
        url = "https://github.com/fastapi/fastapi/issues"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.IssuePullRequestTitle-module__ListItemTitle_1--FWLq8"))
        )

        issue_links = driver.find_elements(By.CSS_SELECTOR, "a.IssuePullRequestTitle-module__ListItemTitle_1--FWLq8")

        for link_el in issue_links[:limit]:
            title = link_el.text.strip()
            tasks.append({
                "title": title,
                "description": "Task imported from Github",
            })

    finally:
        driver.quit()

    return tasks
