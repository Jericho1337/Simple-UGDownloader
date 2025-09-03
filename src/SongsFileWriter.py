# CLASS THAT PRODUCES PDF AND TXT OUTPUTS OF TABS

from fpdf import FPDF
import re as regex
import os

class SongsFileWriter:

    NORMAL_CHORD_REGEX = "([CDEFGAB](#|##|b|bb)?)((M|maj|m|aug|dim|sus|add)?(6|7|9|11|13|-5|\+5)?[^cefghilnopqrtuvxyz])" #IDENTIFIES CHORDS IN A NORMAL TEXT
    TRUEMODE_CHORD_REGEX = "(?<=\\\CHORD\[)(.*?)(?=\])"# IDENTIFIES CHORDS IN TRUE MODE: USES POSITIVE AND NEGATIVE REGEX LOOKAHEAD TO RETRIEVE ONLY CHARACTERS INSIDE
    CHORDPRO_CHORD_REGEX = "(?<=\\\CHORD)(\[.*?\])" #IDENTIFIES CHORDS IN CHORDPRO MODE: USES POSITIVE AND NEGATIVE REGEX LOOKAHEAD TO RETRIEVE ONLY CHARACTERS INSIDE
    UNCLEAN_TRUEMODE_CHORD_REGEX = "(\\\CHORD\[)(.*?)(\])" #\CHORD[] GARBAGE PRESENT IN THIS REGEX, IT IS STRUCTURED In 3 REGEX GROUPS -> USE 2nd GROUP TO TAKE THE CHORD ONLY
    UNCLEAN_CHORDPROMODE_CHORD_REGEX = "(\\\CHORD)(\[.*?\])" #\CHORD GARBAGE PRESENT IN THIS REGEX, IT IS STRUCTURED In 2 REGEX GROUPS -> USE 2nd GROUP TO TAKE THE [CHORD] ONLY
    SECTION_REGEX="(?<!\\\CHORD)\[(.*?)\]"
    OUTPUT_PATH = os.path.abspath((os.path.join(os.path.dirname(__file__),"..", "output").replace("\\","/")))

    TITLE_FONT_SIZE = 18
    TEXT_FONT_SIZE = 10

    TITLE_CELL_SIZE = 10
    AUTHOR_CELL_SIZE = 5

    TEXT_HEIGHT_SIZE = 5

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

        #TRUE NORMAL PDF OBJECT
        self.pdf_true_normal = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_true_normal.add_page()

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

        #TRUE NORMAL PDF OBJECT
        self.pdf_true_normal.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_true_normal.add_font(font_name,'B',bold_font_path, uni=True)

    def set_chordline_char_threshold(self, chord_charcount_threshold):
        self.chord_charcount_threshold = chord_charcount_threshold

    def generate_bold_pdf(self, song):
        #WRITE TITLE
        self.pdf_bold.set_font(self.font_name, size = SongsFileWriter.TITLE_FONT_SIZE , style = "B")
        self.pdf_bold.cell(0,SongsFileWriter.TITLE_CELL_SIZE, song.get_title(),align="C")
        self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE AUTHOR
        authors = ""
        for author in song.get_author():
            authors = authors + author + "/"
        authors = authors[:-1] 
        self.pdf_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style = "")
        self.pdf_bold.cell(0,SongsFileWriter.AUTHOR_CELL_SIZE, authors,"B",align="C")
        self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE TUNING, KEY, CAPO
        self.pdf_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE , style = "")
        self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Tuning: "+song.get_tuning()+"\n")
        self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Key: "+song.get_key()+"\n")
        self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Capo: "+song.get_capo()+"\n\n")

        #WRITE TEXT BOLDING CHORD LINES
        for line in (song.get_text()).split("\n"):
            line = line + "\n"
            #CONDITION TO IDENTIFY CHORD LINE: 
            #At least 1 chord is present (using regex) AND charcount excluding whitespaces is less than constant AND there aren't both chars [] 
            if bool(regex.search(SongsFileWriter.NORMAL_CHORD_REGEX,line)) and (len(line) - line.count(" ") < self.chord_charcount_threshold) and not (("[" in line) and ("]" in line)):
                self.pdf_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="B")
            else:
                self.pdf_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
            self.pdf_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line)
        self.pdf_bold.output(os.path.join(SongsFileWriter.OUTPUT_PATH, "boldchords/").replace("\\","/") + song.get_title() + ".pdf")

    def generate_normal_pdf(self, song):

        #WRITE TITLE
        self.pdf_normal.set_font(self.font_name, size = SongsFileWriter.TITLE_FONT_SIZE, style = "B")
        self.pdf_normal.cell(0,SongsFileWriter.TITLE_CELL_SIZE,song.get_title(),align="C")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE AUTHOR
        authors = ""
        for author in song.get_author():
            authors = authors + author + "/"
        authors = authors[:-1] 
        self.pdf_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style = "")
        self.pdf_normal.cell(0,SongsFileWriter.AUTHOR_CELL_SIZE, authors,"B",align="C")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE TUNING, KEY, CAPO
        self.pdf_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE , style = "")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Tuning: "+song.get_tuning()+"\n")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Key: "+song.get_key()+"\n")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Capo: "+song.get_capo()+"\n\n")


        self.pdf_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
        self.pdf_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,song.get_text())
        self.pdf_normal.output(os.path.join(SongsFileWriter.OUTPUT_PATH, "normalchords/").replace("\\","/") + song.get_title() + ".pdf")

    def generate_normal_text(self, song):
        with open(os.path.join(SongsFileWriter.OUTPUT_PATH, "text/").replace("\\","/") + song.get_title() + ".txt", "w", encoding="utf-8") as text_song:
            #WRITE TITLE
            text_song.write(song.get_title())
            text_song.write("\n")
            #WRITE AUTHOR
            authors = ""
            for author in song.get_author():
                authors = authors + author + "/"
            authors = authors[:-1] 
            text_song.write(authors)
            text_song.write("\n\n")
            #WRITE TUNING, KEY, CAPO
            text_song.write("Tuning: "+song.get_tuning()+"\n")
            text_song.write("Key: "+song.get_key()+"\n")
            text_song.write("Capo: "+song.get_capo()+"\n\n")
            #WRITE TEXT
            text_song.write(song.get_text())

    def generate_true_bold_pdf(self, song):
        #WRITE TITLE
        self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TITLE_FONT_SIZE, style = "B")
        self.pdf_true_bold.cell(0,SongsFileWriter.TITLE_CELL_SIZE,song.get_title(),align="C")
        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE AUTHOR
        authors = ""
        for author in song.get_author():
            authors = authors + author + "/"
        authors = authors[:-1] 
        self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style = "")
        self.pdf_true_bold.cell(0,SongsFileWriter.AUTHOR_CELL_SIZE, authors,"B",align="C")
        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE TUNING, KEY, CAPO
        self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE , style = "")
        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Tuning: "+song.get_tuning()+"\n")
        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Key: "+song.get_key()+"\n")
        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Capo: "+song.get_capo()+"\n\n")

        for line in (song.get_true_text()).split("\n"):
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
                            self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="B")
                            self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line[i])
                            found = True
                            break
                    #IF INDEX WAS NOT FOUND IN CHORD CHARATER RANGES IT WILL BE A NORMAR CHARACTER
                    if(not found):
                        self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
                        self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line[i])
            #NORMAL LINE WITHOUT CHORDS
            else:
                self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
                self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line) 

        self.pdf_true_bold.output(os.path.join(SongsFileWriter.OUTPUT_PATH, "true_boldchords/").replace("\\","/") + song.get_title() + ".pdf")
    
    def generate_true_normal_pdf(self, song):
        
        #WRITE TITLE
        self.pdf_true_normal.set_font(self.font_name, size = SongsFileWriter.TITLE_FONT_SIZE, style = "B")
        self.pdf_true_normal.cell(0,SongsFileWriter.TITLE_CELL_SIZE,song.get_title(),align="C")
        self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE AUTHOR
        authors = ""
        for author in song.get_author():
            authors = authors + author + "/"
        authors = authors[:-1] 
        self.pdf_true_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style = "")
        self.pdf_true_normal.cell(0,SongsFileWriter.AUTHOR_CELL_SIZE, authors,"B",align="C")
        self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"\n\n")

        #WRITE TUNING, KEY, CAPO
        self.pdf_true_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE , style = "")
        self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Tuning: "+song.get_tuning()+"\n")
        self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Key: "+song.get_key()+"\n")
        self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,"Capo: "+song.get_capo()+"\n\n")

        self.pdf_true_normal.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="") #SET NORMAL FONT FOR TEXT
        for line in (song.get_true_text()).split("\n"):
            line = line + "\n"
            
            #CHECK IF THERE IS AT LEAST ONE CHORD
            if regex.search(SongsFileWriter.TRUEMODE_CHORD_REGEX, line) != None:
                
                #REMOVE \CHORD[] BEFORE WRITING ON PDF
                line = regex.sub(SongsFileWriter.UNCLEAN_TRUEMODE_CHORD_REGEX,r"\2",line)
                
            self.pdf_true_normal.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line) 

        self.pdf_true_normal.output(os.path.join(SongsFileWriter.OUTPUT_PATH, "true_normalchords/").replace("\\","/") + song.get_title() + ".pdf")
    
    def generate_true_text(self, song):
        with open(os.path.join(SongsFileWriter.OUTPUT_PATH, "true_text/").replace("\\","/") + song.get_title() + ".txt", "w", encoding="utf-8") as text_song:
            #WRITE TITLE
            text_song.write(song.get_title())
            text_song.write("\n")
            #WRITE AUTHOR
            authors = ""
            for author in song.get_author():
                authors = authors + author + "/"
            authors = authors[:-1] 
            text_song.write(authors)
            text_song.write("\n\n")
            #WRITE TUNING, KEY, CAPO
            text_song.write("Tuning: "+song.get_tuning()+"\n")
            text_song.write("Key: "+song.get_key()+"\n")
            text_song.write("Capo: "+song.get_capo()+"\n\n")
            #WRITE TEXT
            text_song.write(song.get_true_text())

    def generate_chordpro_text(self, song):
        with open(os.path.join(SongsFileWriter.OUTPUT_PATH, "chordpro_text/").replace("\\","/") + song.get_title() + ".txt", "w", encoding="utf-8") as text_song:
            #WRITE TITLE
            text_song.write("{title: "+song.get_title()+"}")
            text_song.write("\n")
            #WRITE AUTHOR
            authors = ""
            for author in song.get_author():
                authors = authors + author + "/"
            authors = authors[:-1] 
            text_song.write("{artist: "+authors+"}")
            text_song.write("\n\n")
            #WRITE TUNING, KEY, CAPO (TUNING IS NOT A DEFAULT TAG IN CHORDPRO)
            #text_song.write("Tuning: "+song.get_tuning()+"\n")
            text_song.write("{key: "+song.get_key()+"}\n")
            text_song.write("{capo: "+song.get_capo()+"}\n\n")
            
            #WRITE TEXT
            splitted_text = song.get_true_text().split("\n")
            
            #FIRST CYCLE: CONVERT SECTIONS
            end_section=""
            for line_index, line in enumerate(splitted_text):
                if regex.search(SongsFileWriter.SECTION_REGEX, line) != None:     
                    section = regex.search(SongsFileWriter.SECTION_REGEX, line).group(0)
                    if "chorus" in section.lower():
                        splitted_text[line_index] = end_section + "{start_of_chorus: "+section[1:-1] +"}"
                        end_section = "{end_of_chorus}\n"
                    elif "bridge" in section.lower():
                        splitted_text[line_index] = end_section + "{start_of_bridge: "+section[1:-1] +"}"
                        end_section = "{end_of_bridge}\n"
                    else:
                        splitted_text[line_index] = end_section + "{start_of_verse: "+section[1:-1] +"}"
                        end_section = "{end_of_verse}\n"
            splitted_text.append(end_section) #CLOSES LAST SECTION
            
            #SECOND CYCLE: CONVERT CHORD ON UPLINE INTO CHORD IN SAME LINE AND WRITE LINES INTO FILE
            skip_line = False
            for line_index, line in enumerate(splitted_text):
                if skip_line:
                    skip_line = False
                    continue

                if regex.search(SongsFileWriter.TRUEMODE_CHORD_REGEX, line) != None: #CHECK IF THERE IS AT LEAST ONE CHORD IN LINE
                    matches = regex.finditer(SongsFileWriter.CHORDPRO_CHORD_REGEX,line)
                    list_of_chord_positions_in_line = []
                    list_of_chord_position_in_newline = []
                    match_offset = 0 # USED TO ADJUST MATCH REFERENCES AFTER REMOVAL
                    total_newline_offset = 0 #USED TO MOVE CHORDS IN NEXT LINE
                    #WE GET MATCH RANGES
                    for match in matches:
                        match_offset += 1 #MATCHES ARE IN INCREASING ORDER (STRING IS READ FROM LEFT TO RIGHT)
                        
                        #EVERY CHORD MUST BE SHIFTED ACCORDING TO THIS RULE: 
                        # -> SUBTRACT 6 FOR CURRENT AND EVERY PRECEDENT CHORD FOR THE "\CHORD" STRING 
                        total_line_offset = 6*match_offset #EVERY REFERENCE SHOULD BE ADJUSTED BY THIS TOTAL OFFSET
                        list_of_chord_positions_in_line.append([match.start()-total_line_offset,match.end()-total_line_offset]) #REFERENCES IN CURRENT LINE
                        list_of_chord_position_in_newline.append([match.start()-total_line_offset+total_newline_offset,match.end()-total_line_offset+total_newline_offset]) #REFERENCE IN NEW LINE
                        total_newline_offset += ((match.end()-total_line_offset) - (match.start()-total_line_offset))

                    #REMOVE \CHORD LEAVING ONLY [CHORD]
                    line = regex.sub(SongsFileWriter.UNCLEAN_CHORDPROMODE_CHORD_REGEX,r"\2",line)
                    nextline = splitted_text[line_index+1]

                    #PADDING NEXT LINE TO ACTUAL LINE LENGTH IF NEXT LINE IS SHORTER (CHORDS CAN BE OUT OF TEXT)
                    if(len(line) > len(nextline)):
                        nextline = ("{:<" + str(len(line)) + "}").format(nextline)
                    
                    #GET CHORDS FROM LINE
                    chords_in_line = []
                    for position in list_of_chord_positions_in_line:
                        chords_in_line.append(line[position[0]:(position[1])])
                    
                    #INSERT CHORDS INTO NEXTLINE
                    nextline = list(nextline) #CONVERTING TO LIST BECAUSE STRINGS ARE IMMUTABLE
                    for chord_index, chord in enumerate(chords_in_line):
                        nextline.insert(list_of_chord_position_in_newline[chord_index][0],chord) 
                    nextline = "".join(nextline) #RECONVERTING TO STRING
                    skip_line = True #SKIP NEXTLINE WHEN BECOMES LINE IN NEXT CYCLE

                    #MERGE LINES INSERTING ONLY NEXT LINE
                    text_song.write(nextline+"\n")
                else:
                    text_song.write(line+"\n")

                

    """"
        for line in (song.get_true_text()).split("\n"):
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
                                self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="B")
                                self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line[i])
                                found = True
                                break
                        #IF INDEX WAS NOT FOUND IN CHORD CHARATER RANGES IT WILL BE A NORMAR CHARACTER
                        if(not found):
                            self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
                            self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line[i])
                #NORMAL LINE WITHOUT CHORDS
                else:
                    self.pdf_true_bold.set_font(self.font_name, size = SongsFileWriter.TEXT_FONT_SIZE, style="")
                    self.pdf_true_bold.write(SongsFileWriter.TEXT_HEIGHT_SIZE,line) 

            self.pdf_true_bold.output(os.path.join(SongsFileWriter.OUTPUT_PATH, "true_boldchords/").replace("\\","/") + song.get_title() + ".pdf")
    """
