from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#CLASS THAT NAVIGATES WEBPAGES USING SELENIUM AND RETURNS SONG INFORMATIONS (text with chords, title, ...)

class WebNavigator:

    def __init__(self):
        self.edge_options = Options()
        self.edge_options.add_argument("--headless=new")
        self.edge_options.add_argument("disable-infobars")
        self.edge_options.add_argument("--disable-extensions")
        self.edge_options.add_argument('--no-sandbox')
        self.edge_options.add_argument('--disable-application-cache')
        self.edge_options.add_argument('--disable-gpu')
        self.edge_options.add_argument("--disable-dev-shm-usage")
        self.edge_options.add_argument("--start-maximized")
        self.edge_options.add_argument('log-level=3')
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