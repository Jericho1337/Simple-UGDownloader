from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from . import Song

#CLASS THAT NAVIGATES WEBPAGES USING SELENIUM AND RETURNS SONG INFORMATIONS (text with chords, title, ...)

class WebNavigator:

    SUPPORTED_BROWSER = ["Edge","Chrome","Firefox"] 

    def __init__(self,browser):
        
        #INIT BROWSER ACCORDING TO CHOSEN ONE
        if(browser == "Edge"):
            self.edge_options = EdgeOptions()
            self.edge_options.add_argument("--headless=new")
            self.edge_options.add_argument("--disable-infobars")
            self.edge_options.add_argument("--disable-extensions")
            self.edge_options.add_argument('--no-sandbox')
            self.edge_options.add_argument('--disable-application-cache')
            self.edge_options.add_argument('--disable-gpu')
            self.edge_options.add_argument("--disable-dev-shm-usage")
            self.edge_options.add_argument("--start-maximized")
            self.edge_options.add_argument('--log-level=3')
            self.edge_options.add_experimental_option("detach", True)
            self.driver = webdriver.Edge(self.edge_options)
            self.driver.implicitly_wait(10)

        elif(browser == "Chrome"):
            self.chrome_options = ChromeOptions()
            self.chrome_options.add_argument("--headless=new")
            self.chrome_options.add_argument("--disable-infobars")
            self.chrome_options.add_argument("--disable-extensions")
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-application-cache')
            self.chrome_options.add_argument('--disable-gpu')
            self.chrome_options.add_argument("--disable-dev-shm-usage")
            self.chrome_options.add_argument("--start-maximized")
            self.chrome_options.add_argument('--log-level=3')
            self.chrome_options.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome(self.chrome_options)
            self.driver.implicitly_wait(10)
        
        elif(browser == "Firefox"):
            self.firefox_options = FirefoxOptions()
            self.firefox_options.add_argument("--headless")
            self.firefox_options.add_argument("--disable-infobars")
            self.firefox_options.add_argument("--disable-extensions")
            self.firefox_options.add_argument('--no-sandbox')
            self.firefox_options.add_argument('--disable-application-cache')
            self.firefox_options.add_argument('--disable-gpu')
            self.firefox_options.add_argument("--disable-dev-shm-usage")
            self.firefox_options.add_argument("--start-maximized")
            self.firefox_options.add_argument('--log-level=3')
            self.driver = webdriver.Firefox(self.firefox_options)
            self.driver.implicitly_wait(10)

        else:
            raise Exception("Cannot find browser " + browser)
    
    def get_song_from_webpage(self, url):
        song = Song.Song()
        self.driver.get(url)

        song.set_title(self.get_song_title())
        song.set_author(self.get_song_author())
        song.set_text(self.get_song_text_and_chords())
        song.set_true_text(self.get_true_song_text_and_chords())

        return song

    def get_song_title(self):
        HTML_title = self.driver.find_element(By.TAG_NAME, "h1")
        return HTML_title.text
    
    def get_song_author(self):
        try:
            authors_text = []
            HTML_title_parent = self.driver.find_element(By.XPATH, "//h1//parent::div")
            HTML_authors = HTML_title_parent.find_elements(By.TAG_NAME, "a")
            for HTML_author in HTML_authors:
                authors_text.append(HTML_author.text)
            return authors_text
        except:
            return []
    
    def get_song_text_and_chords(self):
        HTML_text = self.driver.find_element(By.TAG_NAME, "pre")
        return HTML_text.text
    
    def get_true_song_text_and_chords(self):
        HTML_text = self.driver.find_element(By.TAG_NAME, "pre")
        #EXPLANATION: ULTIMATE GUITAR FORMATS CHORDS ONLY IN THE PARTIAL VIEW OF BROWSER, SO WE HAVE 2 OPTIONS
        #1. SCROLL PAGE GRADUALLY AND FORMAT CHORDS (NOT CHOSEN METHOD: TOO DIFFICULT AND PRONE TO BUGS)
        #2. ZOOM OUT TO A REALLY LITTLE ZOOM RATIO (0.01) TO VIEW ALL CHORDS TOGETHER (CHOSEN METHOD)
        # SINCE FORMATTING OF CHORD JAVASCRIPT IS TRIGGERED BY SCROLL, WE NEED ZOOM OUT AND SCROLL DOWN IN MORE STEPS -> IF WE JUMP DIRECTLY TO 0.01 WE CAN'T SCROLL DOWN BECAUSE PAGE IS TOO LITTLE AND ISN'T SCROLLABLE ANYMORE
        # USING A FOR WE GRADUALLY ZOOM OUT AND GIVE A LITTLE SCROLL TO ACTIVE JAVASCRIPT FORMATTING (0.81 and SCROLL -> 0.61 and SCROLL -> 0.41 and SCROLL -> 0.21 and SCROLL -> 0.01 and SCROLL)
        for i in range (0,5):
            self.driver.execute_script("document.body.style.zoom = '0."+str(8-i*2)+"1'")
            ActionChains(self.driver).scroll_by_amount(0,10).perform()
        chord_list = HTML_text.find_elements(By.CSS_SELECTOR, "span[data-name]") #in PRE tag, there are SPAN tags that use the attribute [data-name="<CHORD>""] and we use this to identify chords
        if chord_list != None:
            for chord in chord_list:
                #WE FORMAT CHORDS AS "\CHORD[<CHORD>] SO WE CAN POSTPROCESS IT" 
                self.driver.execute_script("arguments[0].innerText =  '\\\CHORD[' + arguments[0].innerText + ']'", chord)
        return HTML_text.text
  
    def __del__(self):
        self.driver.quit()