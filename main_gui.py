from src import SongsFileReader
from src import WebNavigator
from src import SongsFileWriter
from src import ConfigFileReader
import os
import re
from threading import Thread
import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import sv_ttk
from tkinter import filedialog


###===================================CONFIG PARAMETERS===================================###

config_file_path = "config/config.yaml"
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

###===================================WINDOW PROGRAMMING LOGIC HELP FUNCTIONS===================================###

def print_to_textbox(text):
    console_output.configure(state="normal")
    console_output.insert(tkinter.END, text)
    console_output.see(tkinter.END)
    console_output.configure(state="disabled")
    console_output.see(tkinter.END)

def button_download_press():
    song_downloader_thread = Thread(target=main)
    song_downloader_thread.start()

def increment_progressbar(value):
    progress_bar['value'] += value

def set_progressbar(percentage):
    progress_bar['value'] = percentage

def open_filepath():
    filepath = filedialog.askopenfilename(title="Open URL song input file", initialdir="/", filetypes=(('text files', '*.txt'), ('All files', '*.*')))
    filepath = filepath.replace("\\","/")
    if(filepath != ""):
        inputpath_text.configure(state="normal")
        inputpath_text.delete(1.0,tkinter.END)
        inputpath_text.insert(tkinter.END, filepath)
        inputpath_text.configure(state="disabled")

###===================================WINDOW INTERFACE DESIGN===================================###


#WINDOW OPTIONS
window = tkinter.Tk()
window.title("Simple UG Downloader")
window_icon = tkinter.PhotoImage("images/icon.png")
window.iconphoto(False, window_icon)
window.resizable(False, False)

#BROWSER LABEL
browser_label = tkinter.Label(window, text = "Preferred Browser: ", font=("Helvetica",12))
browser_label.grid(row=0, column=0, sticky="E", padx=10, pady=10)
#BROWSER COMBOBOX
browser_variable = tkinter.StringVar()
browser_combobox = ttk.Combobox(window, textvariable= browser_variable, state="readonly")
browser_combobox['values'] = ("Edge","Chrome","Firefox")
browser_combobox.grid(row=0, column=1, sticky="WE",pady=10)
browser_combobox.current(browser_combobox["values"].index(browser))

#ACCIDENTAL LABEL
accidental_label = tkinter.Label(window, text = "Accidental: ", font=("Helvetica",12))
accidental_label.grid(row=1, column=0, sticky="E", padx=10, pady=10)
#ACCIDENTAL COMBOBOX
accidental_variable = tkinter.StringVar()
accidental_combobox = ttk.Combobox(window, textvariable= accidental_variable, state="readonly")
accidental_combobox['values'] = ("o","#","b")
accidental_combobox.grid(row=1, column=1, sticky="WE",pady=10)
accidental_combobox.current(accidental_combobox['values'].index(accidental))

#TRANSPOSE LABEL
transpose_label = tkinter.Label(window, text = "Transpose offset: ", font=("Helvetica",12))
transpose_label.grid(row=2, column=0, sticky="E", padx=10, pady=10)
#TRANSPOSE SPINBOX
transpose_spinbox = ttk.Spinbox(window, from_=-12, to=12, width=3, font=("Helvetica", 12), state="readonly")
transpose_spinbox.grid(row=2, column=1,sticky="W",pady=10)
transpose_spinbox.delete(0,tkinter.END)
transpose_spinbox.configure(state="normal")
transpose_spinbox.insert(0,0)
transpose_spinbox.configure(state="readonly")

#INPUT PATH LABEL
inputpath_label = tkinter.Label(window, text = "Input file: ", font=("Helvetica",12))
inputpath_label.grid(row=3, column=0, sticky="E", padx=10, pady=10)
#INPUT PATH TEXTBOX
inputpath_text = ScrolledText(width=60, height= 1)
inputpath_text.grid(row=3, column=1, columnspan=2, sticky="W", padx=10, pady=10)
inputpath_text.insert(tkinter.END, songs_to_download_file)
inputpath_text.configure(state="disabled")
#INPUT PATH BUTTON 
inputpath_button = tkinter.Button(text="...", command=open_filepath)
inputpath_button.grid(row=3, column=3, sticky="W", padx=10, pady=10)

#DOWNLOAD BUTTON OPTIONS
download_button = tkinter.Button(text="Download", command=button_download_press)
download_button.grid(row=4, column=7, padx=10, pady=10)

#PROGRESS BAR
progress_bar = ttk.Progressbar(length=770)
progress_bar.grid(row=5, column=0, columnspan=10)

#CONSOLE OUTPUT
console_output = ScrolledText(width=85, height=18)
console_output.grid(row=6, column=0, columnspan=8, sticky="WE", padx=10, pady=10)
console_output.configure(state="disabled")

#SET THEME
sv_ttk.set_theme("dark")

###===================================WINDOW PROGRAMMING LOGIC===================================###

#Cleans .pkl files in fonts folder because .pkl files cache paths and can cause problems
def cleanup():
    font_dir = os.path.join(os.path.dirname(__file__), "fonts").replace("\\","/")
    font_files = os.listdir(font_dir)

    for f in font_files:
        if re.search(r"(.*?).pkl", f):
            os.remove(os.path.join(font_dir, f).replace("\\","/"))

def main():

    cleanup() #REMOVES TEMPORARY FILES BEFORE EXECUTION

    #RETRIEVE DATA FROM WINDOW INPUT FIELDS
    browser=browser_combobox.get()
    accidental=accidental_combobox.get()
    chord_transpose_offset=int(transpose_spinbox.get())
    songs_to_download_file=inputpath_text.get("1.0",tkinter.END).replace("\n","")

    #OPEN INPUT URL SONG LIST FILE
    songreader = SongsFileReader.SongsFileReader(songs_to_download_file)
    songs_to_download_urllist = songreader.get_url_list()
    songs_to_download_transposelist = songreader.get_transpose_list()

    #START WEBDRIVER WITH PREFERRED BROWSER
    try:
        print_to_textbox("[          ] 0% Starting " + browser + " browser\n")
        webnavigator = WebNavigator.WebNavigator(browser)
    except Exception:
        #TRY REMAINING SUPPORTED WEB BROWSERS
        print_to_textbox("[          ] 0% Browser "+ browser +" failed!\n")
        supported_browsers = WebNavigator.WebNavigator.SUPPORTED_BROWSERS # GET LIST OF SUPPORTED BROWSERS
        supported_browsers.remove(browser) #REMOVE SUPPORTED BROWSER
        
        for selected_browser in supported_browsers: #TRY STARTING OTHER BROWSERS
            print_to_textbox("[          ] 0% Starting " + selected_browser + " browser...\n")
            try:
                webnavigator = WebNavigator.WebNavigator(selected_browser) #TRY NEXT BROWSER IN LIST  
                break #IF BROWSER STARTED BREAK TRY FOR CYCLE
            except Exception:
                print_to_textbox("[          ] 0% Browser "+ selected_browser +" failed!\n")

    #DOWNLOAD EACH SONG
    progress_bar_increment = 10.0/len(songs_to_download_urllist)
    for song_index, url_line in enumerate(songs_to_download_urllist):

        try:
            
            #GET SONG FROM WEBPAGE
            print_to_textbox("[=         ] 10% Getting webpage...\n")
            increment_progressbar(progress_bar_increment)
            song = webnavigator.get_song_from_webpage(url_line)

            #TRANSPOSE TEXT: WE USE TRUE TRANSPOSE FOR TRUE AND NORMAL TRANSPOSE FOR NORMAL
            total_chord_transpose_offset = songs_to_download_transposelist[song_index] + chord_transpose_offset #ADDS OFFSET FROM CMD ARGUMENT TO OFFSET SPECIFIED IN INPUT FILE
            print_to_textbox("[==        ] 20% Transposing song by "+ str(total_chord_transpose_offset) +" offset...\n")
            increment_progressbar(progress_bar_increment)
            song.transpose(total_chord_transpose_offset, accidental)
            song.true_transpose(total_chord_transpose_offset, accidental)

            #GENERATE OUTPUTS
            songwriter = SongsFileWriter.SongsFileWriter()
            songwriter.add_font(font_name, normal_font_path, bold_font_path)
            songwriter.set_chordline_char_threshold(chord_charcount_exclusion)

            #NORMAL MODE OUTPUTS
            print_to_textbox("[===       ] 30% Generating chords bold PDF for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_bold_pdf(song)
            print_to_textbox("[====      ] 40% Generating chords normal PDF for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_normal_pdf(song)
            print_to_textbox("[=====     ] 50% Generating chords normal TXT for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_normal_text(song)

            #TRUE MODE OUTPUTS
            print_to_textbox("[======    ] 60% Generating chords TRUE bold PDF for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_true_bold_pdf(song)
            print_to_textbox("[=======   ] 70% Generating chords TRUE bold PDF for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_true_normal_pdf(song)
            print_to_textbox("[========  ] 80% Generating chords TRUE TXT for "+ song.get_title() +"...\n" )
            increment_progressbar(progress_bar_increment)
            songwriter.generate_true_text(song)

            print_to_textbox("[========= ] 90% Generating chordpro TXT for "+ song.get_title() +"...\n")
            increment_progressbar(progress_bar_increment)
            songwriter.generate_chordpro_text(song)

            print_to_textbox("[==========] 100% Completed " + song.get_title() + " download\n")
            increment_progressbar(progress_bar_increment)
        except Exception as exception:
            print_to_textbox("Song: " + url_line + " failed to download\n")
            print_to_textbox(exception)

    #SET PROGRESS BAR TO 100%
    set_progressbar(100.0)

    #DESTROY TEMP FILES
    cleanup()

if __name__ == "__main__":
    window.mainloop()



