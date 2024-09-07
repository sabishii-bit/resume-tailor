import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class WorkdayScraper:
    def __init__(self, url: str):
        self.url = url
        self.job_description = None

    def validate_url(self) -> bool:
        """Validate if the URL is a Workday application page."""
        pattern = r'wd\d+\.myworkdayjobs\.com'
        if re.search(pattern, self.url):
            return True
        else:
            print(f"Invalid Workday URL: {self.url}")
            return False

    def scrape_job_description(self):
        """Scrape the job description from the Workday page."""
        if not self.validate_url():
            return

        driver = None
        try:
            # Set up Firefox options and driver
            firefox_options = Options()
            firefox_options.add_argument("--headless")  # Run in headless mode
            driver = webdriver.Firefox(options=firefox_options)  # No need to specify GeckoDriver path now

            # Load the page
            driver.get(self.url)

            # Wait for the page to load the job description
            time.sleep(5)  # Increase wait time if the page is slower

            # Find the job description element
            job_desc_element = driver.find_element(By.CSS_SELECTOR, 'div[data-automation-id="jobPostingDescription"]')

            if job_desc_element:
                self.job_description = job_desc_element.text.strip()
                print(f"Job Description Captured:\n{self.job_description[:500]}...")  # Truncate output for readability
            else:
                raise ValueError("Job description element not found on the page.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if driver:
                driver.quit()  # Close the browser

    def get_job_description(self):
        """Return the scraped job description."""
        if self.job_description:
            return self.job_description
        else:
            print("No job description found. Have you scraped the page?")
            return None

# Example usage:
if __name__ == "__main__":
    url = "https://pixar.wd5.myworkdayjobs.com/en-US/Pixar_External_Career_Site/details/Software-Engineer--Tools-GPU--Core-_R-03785"
    scraper = WorkdayScraper(url)
    scraper.scrape_job_description()
    description = scraper.get_job_description()

    if description:
        # Do something with the job description (e.g., process it further or store it)
        print(f"Full Job Description:\n{description}")
