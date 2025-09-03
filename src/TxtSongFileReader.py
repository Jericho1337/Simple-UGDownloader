#CLASS THAT READS A TXT SONG FILE WITH CHORDS AND RETURNS ITS TITLE AND TEXT (USED FOR TXT TO PDF FEATURE)

class TxtSongFileReader:

    def __init__(self, path):   
        self.text_title = ""
        self.author = ""
        self.tuning = ""
        self.key = ""
        self.capo = ""
        self.text_with_chords = ""
        with open(path, "r") as song_file:
            self.text_title = song_file.readline().replace("\n","") #FIRST LINE IS TITLE
            self.author = song_file.readline().replace("\n","") #SECOND LINE IS AUTHOR
            song_file.readline() # SKIP EMPTY LINE
            self.tuning = song_file.readline().replace("\n","").replace("Tuning: ", "") #FOURTH LINE IS TUNING
            self.key = song_file.readline().replace("\n","").replace("Key: ", "") #FIFTH LINE IS KEY
            self.capo = song_file.readline().replace("\n","").replace("Capo: ", "") #SIXTH LINE IS CAPO

            for line in song_file:
                self.text_with_chords = self.text_with_chords + line #OTHER LINES ARE SONG TEXT

    def get_text_title(self):
        return self.text_title
    
    def get_text_with_chords(self):
        return self.text_with_chords
    
    def get_author(self):
        return self.author
    
    def get_tuning(self):
        return self.tuning
    
    def get_key(self):
        return self.key
    
    def get_capo(self):
        return self.capo