#CLASS THAT READS A TXT SONG FILE WITH CHORDS AND RETURNS ITS TITLE AND TEXT (USED FOR TXT TO PDF FEATURE)

class TxtSongFileReader:

    def __init__(self, path):
        self.text_with_chords = ""
        self.text_title = ""
        with open(path, "r") as song_file:
            is_first_line = True
            for line in song_file:
                if(is_first_line == True):
                    self.text_title = line.replace("\n","")
                    is_first_line = False
                else:
                    self.text_with_chords = self.text_with_chords + line

    def get_text_title(self):
        return self.text_title
    
    def get_text_with_chords(self):
        return self.text_with_chords