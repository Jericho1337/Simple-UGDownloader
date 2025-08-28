# CLASS THAT PRODUCES PDF AND TXT OUTPUTS OF TABS

from fpdf import FPDF
import re as regex

class SongsFileWriter:

    NORMAL_CHORD_REGEX = "([CDEFGAB](#|##|b|bb)?)((M|maj|m|aug|dim|sus|add)?(6|7|9|11|13|-5|\+5)?[^cefghilnopqrtuvxyz])" #IDENTIFIES CHORDS IN A NORMAL TEXT
    TRUEMODE_CHORD_REGEX = "(?<=\\\CHORD\[)(.*?)(?=\])"# IDENTIFIES CHORDS IN TRUE MODE: USES POSITIVE AND NEGATIVE REGEX LOOKAHEAD TO RETRIEVE ONLY CHARACTERS INSIDE
    UNCLEAN_TRUEMODE_CHORD_REGEX = "(\\\CHORD\[)(.*?)(\])" #\CHORD[] GARBAGE PRESENT IN THIS REGEX, IT IS STRUCTURED In 3 REGEX GROUPS -> USE 2nd GROUP TO TAKE THE CHORD ONLY

    def __init__(self):

        self.font_name = ""
        self.normal_font_path = ""
        self.bold_font_path = ""
        self.chord_charcount_threshold = 15

        #BOLD PDF OBJECT
        self.pdf_bold = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_bold.add_page()

        #NORMAL PDF OBJECT
        self.pdf_normal = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_normal.add_page()

        #TRUE BOLD PDF OBJECT
        self.pdf_true_bold = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_true_bold.add_page()

    def add_font(self, font_name, normal_font_path, bold_font_path):
    
        self.font_name = font_name
        self.normal_font_path = normal_font_path
        self.bold_font_path = bold_font_path

        #BOLD PDF OBJECT
        self.pdf_bold.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_bold.add_font(font_name,'B',bold_font_path, uni=True)

        #NORMAL PDF OBJECT
        self.pdf_normal.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_normal.add_font(font_name,'B',bold_font_path, uni=True)

        #TRUE BOLD PDF OBJECT
        self.pdf_true_bold.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_true_bold.add_font(font_name,'B',bold_font_path, uni=True)

    def set_chordline_char_threshold(self, chord_charcount_threshold):
        self.chord_charcount_threshold = chord_charcount_threshold
             
    def generate_bold_pdf(self, text_title, text_with_chords):    
        
        #WRITE TITLE
        self.pdf_bold.set_font(self.font_name, size = 18, style = "B")
        self.pdf_bold.cell(0,10,text_title,"B",align="C")
        self.pdf_bold.write(5,"\n\n\n")

        #WRITE TEXT BOLDING CHORD LINES
        for line in text_with_chords.split("\n"):
            line = line + "\n"
            #CONDITION TO IDENTIFY CHORD LINE: 
            #At least 1 chord is present (using regex) AND charcount excluding whitespaces is less than constant AND there aren't both chars [] 
            if bool(regex.search(SongsFileWriter.NORMAL_CHORD_REGEX,line)) and (len(line) - line.count(" ") < self.chord_charcount_threshold) and not (("[" in line) and ("]" in line)):
                self.pdf_bold.set_font(self.font_name, size = 10, style="B")
            else:
                self.pdf_bold.set_font(self.font_name, size = 10, style="")
            self.pdf_bold.write(5,line)
        self.pdf_bold.output("./output/boldchords/" + text_title + ".pdf")

    def generate_normal_pdf(self,text_title, text_with_chords):

        self.pdf_normal.set_font(self.font_name, size = 18, style = "B")
        self.pdf_normal.cell(0,10,text_title,"B",align="C")
        self.pdf_normal.write(5,"\n\n\n")
        self.pdf_normal.set_font(self.font_name, size = 10, style="")
        self.pdf_normal.write(5,text_with_chords)
        self.pdf_normal.output("./output/normalchords/" + text_title + ".pdf")

    def generate_normal_text(self, text_title, text_with_chords):
        with open("./output/text/" + text_title + ".txt", "w") as text_song:
            text_song.write(text_title)
            text_song.write("\n\n")
            text_song.write(text_with_chords)

    def generate_true_text(self, text_title, true_text_with_chords):
        with open("./output/true_text/" + text_title + ".txt", "w") as text_song:
            text_song.write(text_title)
            text_song.write("\n\n")
            text_song.write(true_text_with_chords)
    
    def generate_true_bold_pdf(self,text_title, true_text_with_chords):
        self.pdf_true_bold.set_font(self.font_name, size = 18, style = "B")
        self.pdf_true_bold.cell(0,10,text_title,"B",align="C")
        self.pdf_true_bold.write(5,"\n\n\n")

        for line in true_text_with_chords.split("\n"):
            line = line + "\n"
            
            #CHECK IF THERE IS AT LEAST ONE MATCH
            if regex.search(SongsFileWriter.TRUEMODE_CHORD_REGEX, line) != None:
                matches = regex.finditer(SongsFileWriter.TRUEMODE_CHORD_REGEX,line)
                list_of_chord_positions_in_line = []
                match_offset = 0 # USED TO ADJUST MATCH REFERENCES AFTER REMOVAL
                #WE GET MATCH RANGES
                for match in matches:
                    match_offset += 1 #MATCHES ARE IN INCREASING ORDER (STRING IS READ FROM LEFT TO RIGHT)
                    #EVERY CHORD MUST BE SHIFTED ACCORDING TO THIS RULE: 
                    # -> SUBTRACT 7 FOR CURRENT AND EVERY PRECEDENT CHORD FOR THE "\CHORD[" STRING 
                    # -> SUBTRACT 1 FOR EACH PRECEDENT CHORD EXCLUDING CURRENT FOR "]" STRING
                    total_line_offset = 7*match_offset+1*(match_offset-1) #EVERY REFERENCE SHOULD BE ADJUSTED BY THIS TOTAL OFFSET
                    list_of_chord_positions_in_line.append([match.start()-total_line_offset,match.end()-total_line_offset])

                #REMOVE \CHORD[] BEFORE BOLDING
                line = regex.sub(SongsFileWriter.UNCLEAN_TRUEMODE_CHORD_REGEX,r"\2",line)
                
                #ITERATE EACH CHARATER (the indexes) OF THE LINE
                for i in range(0, len(line)):
                    #WE INSPECT IF INDEX IS IN EVERY MATCH RANGE
                    found = False
                    for position in list_of_chord_positions_in_line:
                        #IF INDEX IS IN RANGE IT IS A CHORD CHARACTER AND MUST BE BOLD
                        if i in range(position[0], position[1]):
                            self.pdf_true_bold.set_font(self.font_name, size = 10, style="B")
                            self.pdf_true_bold.write(5,line[i])
                            found = True
                            break
                    #IF INDEX WAS NOT FOUND IN CHORD CHARATER RANGES IT WILL BE A NORMAR CHARACTER
                    if(not found):
                        self.pdf_true_bold.set_font(self.font_name, size = 10, style="")
                        self.pdf_true_bold.write(5,line[i])
            #NORMAL LINE WITHOUT CHORDS
            else:
                self.pdf_true_bold.set_font(self.font_name, size = 10, style="")
                self.pdf_true_bold.write(5,line) 

        self.pdf_true_bold.output("./output/true_boldchords/" + text_title + ".pdf")