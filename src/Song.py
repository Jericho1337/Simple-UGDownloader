# CLASS THAT CONTAINS ALL INFORMATIONS OF A SONG

class Song:

    def __init__(self, title="", author = [], tuning ="", key="", capo="", text="", true_text=""):
        self.title = title
        self.author = author
        self.tuning = tuning
        self.key = key
        self.capo = capo
        self.text = text
        self.true_text = true_text

    #SETTERS
    def set_title(self, title):
        self.title = title

    def set_author(self, author):
        self.author = author

    def set_tuning(self, tuning):
        self.tuning = tuning
    
    def set_key(self, key):
        self.key = key
    
    def set_capo(self, capo):
        self.capo = capo
    
    def set_text(self, text):
        self.text = text
    
    def set_true_text(self, true_text):
        self.true_text = true_text
    
    ##GETTERS##
    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_tuning(self):
        return self.tuning
    
    def get_key(self):
        return self.key
    
    def get_capo(self):
        return self.capo
    
    def get_text(self):
        return self.text
    
    def get_true_text(self):
        return self.true_text