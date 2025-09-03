from src import SongsFileReader
from src import WebNavigator
from src import SongsFileWriter
from src import ConfigFileReader
from src import ChordTransposer
from src import TxtSongFileReader
from src import Colour
from src import Song
import sys
import getopt
import os
import re

config_file_path = "config/config.yaml"

#Cleans .pkl files in fonts folder because .pkl files cache paths and can cause problems
def cleanup():
    font_dir = os.path.join(os.path.dirname(__file__), "fonts").replace("\\","/")
    font_files = os.listdir(font_dir)

    for f in font_files:
        if re.search(r"(.*?).pkl", f):
            os.remove(os.path.join(font_dir, f).replace("\\","/"))

if __name__ == "__main__":

    cleanup() #REMOVES TEMPORARY FILES BEFORE EXECUTION

    project_dir = os.path.join(os.path.dirname(__file__)).replace("\\","/")
    config_file = os.path.join(project_dir, config_file_path).replace("\\","/") #CONVERT RELATIVE PATH TO ABSOLUTE

    #LOAD DEFAULT CONFIGURATION PARAMETERS
    config_reader = ConfigFileReader.ConfigFileReader(config_file)
    config_parameters = config_reader.get_configuration_params()
    songs_to_download_file = os.path.join(project_dir,config_parameters["songs_to_download_file"]).replace("\\","/") #CONVERT RELATIVE PATH TO ABSOLUTE
    font_name = config_parameters["font_name"]
    normal_font_path = os.path.join(project_dir,config_parameters["normal_font_path"]).replace("\\","/") #CONVERT RELATIVE PATH TO ABSOLUTE
    bold_font_path = os.path.join(project_dir,config_parameters["bold_font_path"]).replace("\\","/") #CONVERT RELATIVE PATH TO ABSOLUTE
    chord_charcount_exclusion = config_parameters["chord_charcount_exclusion"]
    browser = config_parameters["default_browser"]
    accidental = config_parameters["default_accidental"] 
    chord_transpose_offset = 0

    #READ CMD LINE ARGS
    if len(sys.argv) > 1:
        try:
            arguments_values, values = getopt.getopt(args=sys.argv[1:], shortopts="", longopts=["help","inputfile=", "transpose=", "txt2pdf=", "truetxt2pdf=", "browser=", "accidental=", "cleanoutput"])
            arguments = []
            values = []
            for argument_value in arguments_values:
                arguments.append(argument_value[0])
                values.append(argument_value[1])
            
            #WE DON'T ITERATE ON INPUT ARGUMENTS TO AVOID A PRIORITY BASED ON DIFFERENT INPUT COMBINATION, WE IMPOSE PRIORITY WITH IFs
            if("--help" in arguments):
                print("")
                print("\t--inputfile <STRING> \t\t Specify a path different from default path for input file")
                print("\t--txt2pdf <STRING> \t\t Specify a path to a TXT file (normal mode) to convert in PDF")
                print("\t--truetxt2pdf <STRING> \t\t Specify a path to a TRUE TXT file (true mode) to convert in PDF")
                print("\t--browser <STRING> \t\t Specify a path to a TRUE TXT file (true mode) to convert in PDF \t\t Possible values \"Edge\",\"Chrome\",\"Firefox\"")
                print("\t--transpose <INT> \t\t Specify a offset (positive or negative) to apply for the transposal \t\t ")
                print("\t--accidental <STRING> \t\t Specify an accidental to force in transposition or original song \t\t Possible values \"#\",\"b\"")
                print("\t--cleanoutput \t\t\t Cleans all output files in the subdirectories of output folder")
                print("")
                sys.exit()
            
            if("--inputfile" in arguments):
                songs_to_download_file = values[arguments.index("--inputfile")] #OVERWRITE DEFAULT INPUT VALUE

            if("--transpose" in arguments):
                chord_transpose_offset = int(values[arguments.index("--transpose")]) #OVERWRITE DEFAULT 0 TRANSPOSE OFFSET
            
            if("--browser" in arguments):
                browser = values[arguments.index("--browser")]

            if("--accidental" in arguments):
                accidental = values[arguments.index("--accidental")]

            if("--cleanoutput" in arguments):
                output_dir_path = os.path.join(os.path.dirname(__file__), "output").replace("\\","/")
                specific_output_dirs = os.listdir(output_dir_path)

                for dir in specific_output_dirs:
                    specific_output_dir_path = os.path.join(output_dir_path, dir).replace("\\","/")
                    specific_output_dir_files = os.listdir(specific_output_dir_path)
                    for f in specific_output_dir_files:
                        os.remove(os.path.join(specific_output_dir_path, f).replace("\\","/"))

                sys.exit()            
            
            if("--txt2pdf" in arguments):

                song = Song.Song()

                #READ NORMAL TXT
                txtsongreader = TxtSongFileReader.TxtSongFileReader(values[arguments.index("--txt2pdf")])
                
                #GET SONG INFORMATION FROM NORMAL TXT FILE
                song.set_title(txtsongreader.get_text_title())
                song.set_text(txtsongreader.get_text_with_chords())
                song.set_author([txtsongreader.get_author()])
                song.set_tuning(txtsongreader.get_tuning())
                song.set_key(txtsongreader.get_key())
                song.set_capo(txtsongreader.get_capo())

                #TRANSPOSE TEXT
                song.set_text(ChordTransposer.ChordTransposer.transpose(song.get_text(), chord_transpose_offset, accidental))

                #WRITE NORMAL AND BOLD PDF
                songwriter = SongsFileWriter.SongsFileWriter()
                songwriter.add_font(font_name, normal_font_path, bold_font_path)
                songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
                songwriter.generate_bold_pdf(song)
                songwriter.generate_normal_pdf(song)

                #CLEANUP BEFORE EXIT
                cleanup()

                sys.exit()

            if("--truetxt2pdf" in arguments):

                song = Song.Song()

                #READ TRUE TXT
                txtsongreader = TxtSongFileReader.TxtSongFileReader(values[arguments.index("--truetxt2pdf")])

                #GET SONG INFORMATION FROM TRUE TXT FILE
                song.set_title(txtsongreader.get_text_title())
                song.set_true_text(txtsongreader.get_text_with_chords())
                song.set_author([txtsongreader.get_author()])
                song.set_tuning(txtsongreader.get_tuning())
                song.set_key(txtsongreader.get_key())
                song.set_capo(txtsongreader.get_capo())

                #TRANSPOSE TEXT
                song.set_true_text(ChordTransposer.ChordTransposer.true_transpose(song.get_true_text(), chord_transpose_offset, accidental))

                #WRITE TRUE BOLD PDF
                songwriter = SongsFileWriter.SongsFileWriter()
                songwriter.add_font(font_name, normal_font_path, bold_font_path)
                songwriter.set_chordline_char_threshold(chord_charcount_exclusion)
                songwriter.generate_true_bold_pdf(song)
                songwriter.generate_true_normal_pdf(song)

                #CLEANUP BEFORE EXIT
                cleanup()

                sys.exit()

        except getopt.error as err:
            print("[ERROR] Unrecognized arguments " + str(err))      

    #OPEN INPUT URL SONG LIST FILE
    songreader = SongsFileReader.SongsFileReader(songs_to_download_file)
    songs_to_download_urllist = songreader.get_url_list()
    songs_to_download_transposelist = songreader.get_transpose_list()

    #START WEBDRIVER
    webnavigator = WebNavigator.WebNavigator(browser)

    #DOWNLOAD EACH SONG
    for song_index, url_line in enumerate(songs_to_download_urllist):

        try:

            #GET SONG FROM WEBPAGE
            print(Colour.Colour.YELLOW + "[=         ] 10% Getting webpage...")
            song = webnavigator.get_song_from_webpage(url_line)

            #TRANSPOSE TEXT: WE USE TRUE TRANSPOSE FOR TRUE AND NORMAL TRANSPOSE FOR NORMAL
            total_chord_transpose_offset = songs_to_download_transposelist[song_index] + chord_transpose_offset #ADDS OFFSET FROM CMD ARGUMENT TO OFFSET SPECIFIED IN INPUT FILE
            print("[=====     ] 50% Transposing song by "+ str(total_chord_transpose_offset) +" offset...")
            song.set_text(ChordTransposer.ChordTransposer.transpose(song.get_text(), total_chord_transpose_offset, accidental))
            song.set_true_text(ChordTransposer.ChordTransposer.true_transpose(song.get_true_text(), total_chord_transpose_offset, accidental))

            #GENERATE OUTPUTS
            songwriter = SongsFileWriter.SongsFileWriter()
            songwriter.add_font(font_name, normal_font_path, bold_font_path)
            songwriter.set_chordline_char_threshold(chord_charcount_exclusion)

            #NORMAL MODE OUTPUTS
            print("[=======   ] 70% Generating chords PDFs and TXT for "+ song.get_title() +"...")
            songwriter.generate_bold_pdf(song)
            songwriter.generate_normal_pdf(song)
            songwriter.generate_normal_text(song)

            #TRUE MODE OUTPUTS
            print("[========= ] 90% Generating TRUE chords PDFs and TXT for "+ song.get_title() +"..." + Colour.Colour.ENDC)
            songwriter.generate_true_bold_pdf(song)
            songwriter.generate_true_normal_pdf(song)
            songwriter.generate_true_text(song)

            print(Colour.Colour.GREEN + Colour.Colour.BOLD + "[==========] 100% Completed " + song.get_title() + " download" + Colour.Colour.ENDC)

        except Exception as exception:
            print(Colour.Colour.RED + "Song: " + url_line + " failed to download" + Colour.Colour.ENDC)
            print(exception)
    
    #DESTROY TEMP FILES
    cleanup()