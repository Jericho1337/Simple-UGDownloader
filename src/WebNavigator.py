from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

#CLASS THAT NAVIGATES WEBPAGES USING SELENIUM AND RETURNS SONGS INFORMATION (text with chords, title, ...)

class WebNavigator:

    def __init__(self):
        self.edge_options = Options()
        self.edge_options.add_argument("--headless")
        self.edge_options.add_argument("disable-infobars")
        self.edge_options.add_argument("--disable-extensions")
        self.edge_options.add_argument('--no-sandbox')
        self.edge_options.add_argument('--disable-application-cache')
        self.edge_options.add_argument('--disable-gpu')
        self.edge_options.add_argument("--disable-dev-shm-usage")
        self.edge_options.add_experimental_option("detach", True)
        self.driver = webdriver.Edge(self.edge_options)
        self.driver.implicitly_wait(10) 
    
    def navigate_webpage(self, url):
        self.driver.get(url)
        
    def get_song_title(self):
        HTML_title = self.driver.find_element(By.TAG_NAME, "h1")
        return HTML_title.text
    
    def get_song_text_and_chords(self):
        HTML_text = self.driver.find_element(By.TAG_NAME, "pre")
        return HTML_text.text
    
    def __del__(self):
        self.driver.quit()