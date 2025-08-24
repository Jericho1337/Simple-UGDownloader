# CLASS THAT PRODUCES PDF AND TXT OUTPUTS OF TABS

from fpdf import FPDF
import re as regex

class SongsFileWriter:

    #CHORD_REGEX = "([CDEFGAB](#|##|b|bb)?)((M|maj|m|aug|dim|sus|add)?(6|7|9|11|13|-5|\+5)?)"
    CHORD_REGEX = "([CDEFGAB](#|##|b|bb)?)((M|maj|m|aug|dim|sus|add)?(6|7|9|11|13|-5|\+5)?[^cefghilnopqrtuvxyz])"

    def __init__(self):

        self.font_name = ""
        self.normal_font_path = ""
        self.bold_font_path = ""
        self.chord_charcount_threshold = 15

        self.pdf_bold = self.pdf_bold = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_bold.add_page()

        self.pdf_normal = self.pdf_normal = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf_normal.add_page()

    def add_font(self, font_name, normal_font_path, bold_font_path):
    
        self.font_name = font_name
        self.normal_font_path = normal_font_path
        self.bold_font_path = bold_font_path

        self.pdf_bold.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_bold.add_font(font_name,'B',bold_font_path, uni=True)

        self.pdf_normal.add_font(font_name, '', normal_font_path, uni=True)
        self.pdf_normal.add_font(font_name,'B',bold_font_path, uni=True)


    def set_chordline_char_threshold(self, chord_charcount_threshold):
        self.chord_charcount_threshold = chord_charcount_threshold
             
    def generate_bold_pdf(self, text_title, text_with_chords):    
        
        self.pdf_bold.set_font(self.font_name, size = 18, style = "B")
        self.pdf_bold.cell(0,10,text_title,"B",align="C")
        self.pdf_bold.write(5,"\n\n\n")

        for line in text_with_chords.split("\n"):
            line = line + "\n"
            #CONDITION TO IDENTIFY CHORD LINE: 
            #At least 1 chord is present (using regex) AND charcount excluding whitespaces is less than constant AND there aren't both chars [] 
            if bool(regex.search(SongsFileWriter.CHORD_REGEX,line)) and (len(line) - line.count(" ") < self.chord_charcount_threshold) and not (("[" in line) and ("]" in line)):
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