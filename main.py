from src import SongsFileReader
from src import WebNavigator
from src import SongsFileWriter
from src import ConfigFileReader
from src import ChordTransposer
from src import TxtSongFileReader
from src import Colour
import sys, getopt

config_file = "input/config.yaml"
whitespaces = "                                          "

if __name__ == "__main__":

    #LOAD DEFAULT CONFIGURATION PARAMETERS
    config_reader = ConfigFileReader.ConfigFileReader(config_file)
    config_parameters = config_reader.get_configuration_params()
    songs_to_download_file = config_parameters["songs_to_download_file"]
    font_name = config_parameters["font_name"]
    normal_font_path = config_parameters["normal_font_path"]
    bold_font_path = config_parameters["bold_font_path"]
    chord_charcount_exclusion = config_parameters["chord_charcount_exclusion"]
    chord_transpose_offset = 0

    #READ CMD LINE ARGS
    if len(sys.argv) > 1:
        try:
            arguments_values, values = getopt.getopt(args=sys.argv[1:], shortopts="i:t:p:", longopts=["inputfile=", "transpose=", "txt2pdf=", "truetxt2pdf="])
            arguments = []
            values = []
            for argument_value in arguments_values:
                arguments.append(argument_value[0])
                values.append(argument_value[1])
            #WE DON'T ITERATE ON INPUT ARGUMENTS TO AVOID A PRIORITY BASED ON DIFFERENT INPUT COMBINATION, WE IMPOSE PRIORITY WITH IFs
            if("--inputfile" in arguments):
                songs_to_download_file = values[arguments.index("--inputfile")] #OVERWRITE DEFAULT INPUT VALUE

            if("--transpose" in arguments):
                chord_transpose_offset = int(values[arguments.index("--transpose")]) #OVERWRITE DEFAULT 0 TRANSPOSE OFFSET
            
            if("--txt2pdf" in arguments):
                #READ NORMAL TXT
                txtsongreader = TxtSongFileReader.TxtSongFileReader(values[arguments.index("--txt2pdf")])
                
                #GET SONG INFORMATION FROM NORMAL TXT FILE
                text_title = txtsongreader.get_text_title()
                text_with_chords = txtsongreader.get_text_with_chords()

                #TRANSPOSE TEXT
                text_with_chords = ChordTransposer.ChordTransposer.transpose(text_with_chords, chord_transpose_offset)

                #WRITE NORMAL AND BOLD PDF
                songwriter = SongsFileWriter.SongsFileWriter()
                songwriter.add_font(font_name, normal_font_path, bold_font_path)
                songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
                songwriter.generate_bold_pdf(text_title, text_with_chords)
                songwriter.generate_normal_pdf(text_title, text_with_chords)
                sys.exit()

            if("--truetxt2pdf" in arguments):
                txtsongreader = TxtSongFileReader.TxtSongFileReader(values[arguments.index("--truetxt2pdf")])

                #GET SONG INFORMATION FROM TRUE TXT FILE
                text_title = txtsongreader.get_text_title()
                true_text_with_chords = txtsongreader.get_text_with_chords()

                #TRANSPOSE TEXT
                true_text_with_chords = ChordTransposer.ChordTransposer.true_transpose(true_text_with_chords, chord_transpose_offset)

                #WRITE TRUE BOLD PDF
                songwriter = SongsFileWriter.SongsFileWriter()
                songwriter.add_font(font_name, normal_font_path, bold_font_path)
                songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
                songwriter.generate_true_bold_pdf(text_title, true_text_with_chords)
                songwriter.generate_true_normal_pdf(text_title, true_text_with_chords)
                sys.exit()

        except getopt.error as err:
            print("[ERROR] Unrecognized arguments " + str(err))      

    #OPEN INPUT URL SONG LIST FILE
    songreader = SongsFileReader.SongsFileReader(songs_to_download_file)
    songs_to_download_urllist = songreader.get_url_list()

    #START WEBDRIVER
    webnavigator = WebNavigator.WebNavigator()

    #DOWNLOAD EACH SONG
    for url_line in songs_to_download_urllist:
        
        try:
            #GET WEBPAGE
            print(Colour.Colour.OKCYAN + "[=         ] 10% Getting webpage..." + whitespaces, end="\r")
            webnavigator.navigate_webpage(url_line)

            #GET SONG TITLE
            print("[==        ] 20% Getting song title..." + whitespaces, end="\r")
            text_title = webnavigator.get_song_title() 

            #GET TEXT AND TRUE TEXT
            print("[===       ] 30% Extracting text and chords for "+ text_title +" from webpage..." + whitespaces, end="\r")
            text_with_chords = webnavigator.get_song_text_and_chords()
            print("[====      ] 40% Extracting TRUE text and chords for "+ text_title +" from webpage..." + whitespaces, end="\r")
            true_text_with_chords = webnavigator.get_true_song_text_and_chords()

            #TRANSPOSE TEXT: WE USE TRUE TRANSPOSE FOR TRUE AND NORMAL TRANSPOSE FOR NORMAL
            print("[=====     ] 50% Transposing song by "+ str(chord_transpose_offset) +" offset..." + whitespaces, end="\r")
            text_with_chords = ChordTransposer.ChordTransposer.transpose(text_with_chords, chord_transpose_offset)
            true_text_with_chords = ChordTransposer.ChordTransposer.true_transpose(true_text_with_chords, chord_transpose_offset)

            #GENERATE OUTPUTS
            songwriter = SongsFileWriter.SongsFileWriter()
            songwriter.add_font(font_name, normal_font_path, bold_font_path)
            songwriter.set_chordline_char_threshold(chord_charcount_exclusion)

            #NORMAL MODE OUTPUTS
            print("[=======   ] 70% Generating chords PDFs and TXT for "+ text_title +"..." + whitespaces, end="\r")
            songwriter.generate_bold_pdf(text_title, text_with_chords)
            songwriter.generate_normal_pdf(text_title, text_with_chords)
            songwriter.generate_normal_text(text_title, text_with_chords)

            #TRUE MODE OUTPUTS
            print("[========= ] 90% Generating TRUE chords PDFs and TXT for "+ text_title +"..." + whitespaces + Colour.Colour.ENDC, end="\r")
            songwriter.generate_true_bold_pdf(text_title, true_text_with_chords)
            songwriter.generate_true_normal_pdf(text_title, true_text_with_chords)
            songwriter.generate_true_text(text_title, true_text_with_chords)

            print(Colour.Colour.OKGREEN + "[==========] 100% Completed " + text_title + " download" + whitespaces + Colour.Colour.ENDC)
        except Exception as exception:
            print("Song: " + url_line + " failed to download" + whitespaces)
            print(exception)