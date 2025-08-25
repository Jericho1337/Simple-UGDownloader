from src import SongsFileReader
from src import WebNavigator
from src import SongsFileWriter
from src import ConfigFileReader
from src import ChordTransposer
import sys, getopt

config_file = "./input/config.yaml"

if __name__ == "__main__":

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
            arguments, values = getopt.getopt(args=sys.argv[1:], shortopts="it:")
            for argument, value in arguments:
                if(argument == "-i"):
                    songs_to_download_file = value #OVERWRITE DEFAULT INPUT VALUE
                if(argument == "-t"):
                    chord_transpose_offset = int(value) #OVERWRITE DEFAULT 0 TRANSPOSE OFFSET 
                
        except getopt.error as err:
            print("[ERROR] Unrecognized arguments " + str(err))      

    #OPEN INPUT URL SONG LIST FILE
    songreader = SongsFileReader.SongsFileReader(songs_to_download_file)
    songs_to_download_urllist = songreader.get_url_list()

    #START WEBDRIVER
    webnavigator = WebNavigator.WebNavigator()

    #DOWNLOAD EACH SONG
    for url_line in songs_to_download_urllist:
        
        #GET WEBPAGE
        print("Getting webpage...")
        webnavigator.navigate_webpage(url_line)

        #GET SONG TITLE
        print("\rGetting song title...")
        text_title = webnavigator.get_song_title() 

        #GET SONG TEXT WITH CHORDS
        print("Extracting text and chords for "+ text_title +" from webpage...")
        text_with_chords = webnavigator.get_song_text_and_chords()

        #TRANSPOSE TEXT
        text_with_chords = ChordTransposer.ChordTransposer.transpose(text_with_chords, chord_transpose_offset)
        
        #GENERATE CHORDS PDF and TXT
        print("Generating chords PDFs and TXT for "+ text_title +"...")

        songwriter = SongsFileWriter.SongsFileWriter()
        songwriter.add_font(font_name, normal_font_path, bold_font_path)
        songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
        songwriter.generate_bold_pdf(text_title, text_with_chords)
        songwriter.generate_normal_pdf(text_title, text_with_chords)
        songwriter.generate_normal_text(text_title, text_with_chords)
