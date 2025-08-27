from src import SongsFileReader
from src import WebNavigator
from src import SongsFileWriter
from src import ConfigFileReader
from src import ChordTransposer
from src import TxtSongFileReader
import sys, getopt

config_file = "./input/config.yaml"

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
    true_mode = False

    #READ CMD LINE ARGS
    if len(sys.argv) > 1:
        try:
            arguments, values = getopt.getopt(args=sys.argv[1:], shortopts="itp:")
            for argument, value in arguments:
                if(argument == "-i"):
                    songs_to_download_file = value #OVERWRITE DEFAULT INPUT VALUE
                if(argument == "-t"):
                    chord_transpose_offset = int(value) #OVERWRITE DEFAULT 0 TRANSPOSE OFFSET
                if(argument == "-p"):
                    txtsongreader = TxtSongFileReader.TxtSongFileReader(value)
                    songwriter = SongsFileWriter.SongsFileWriter()
                    songwriter.add_font(font_name, normal_font_path, bold_font_path)
                    songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
                    songwriter.generate_bold_pdf(txtsongreader.get_text_title(), txtsongreader.get_text_with_chords())
                    songwriter.generate_normal_pdf(txtsongreader.get_text_title(), txtsongreader.get_text_with_chords())
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
        
        #GET WEBPAGE
        print("Getting webpage...")
        webnavigator.navigate_webpage(url_line)

        #GET SONG TITLE
        print("Getting song title...")
        text_title = webnavigator.get_song_title() 

        print("Extracting text and chords for "+ text_title +" from webpage...")
        text_with_chords = webnavigator.get_song_text_and_chords()
        print("Extracting TRUE text and chords for "+ text_title +" from webpage...")
        true_text_with_chords = webnavigator.get_true_song_text_and_chords()

        print("Generating chords PDFs and TXT for "+ text_title +"...")
        songwriter = SongsFileWriter.SongsFileWriter()
        songwriter.add_font(font_name, normal_font_path, bold_font_path)
        songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
        songwriter.generate_bold_pdf(text_title, text_with_chords)
        songwriter.generate_normal_pdf(text_title, text_with_chords)
        songwriter.generate_normal_text(text_title, text_with_chords)

        print("Generating TRUE chords PDFs and TXT for "+ text_title +"...")
        songwriter.generate_true_bold_pdf(text_title, true_text_with_chords)

        #TRANSPOSE TEXT
        #text_with_chords = ChordTransposer.ChordTransposer.transpose(text_with_chords, chord_transpose_offset)

        #GENERATE CHORDS PDF and TXT
           
