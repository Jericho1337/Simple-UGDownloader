import tkinter
from tkinter.scrolledtext import ScrolledText

WIDTH = 670
HEIGHT = 600


def button_download_press():
    console_output.configure(state="normal")
    console_output.insert(tkinter.END, url_textbox.get() + "\n")
    console_output.see(tkinter.END)
    console_output.configure(state="disabled")

#WINDOW OPTIONS
window = tkinter.Tk()
window.geometry(str(WIDTH)+"x"+str(HEIGHT))
window.title("Simple UG Downloader")
window.resizable(False, False)
window.configure(background="white")

#URL LABEL
url_label = tkinter.Label(window, text = "URL: ", font=("Helvetica",15))
url_label.configure(background="white")
url_label.grid(row=0, column=0, sticky="WE", padx=0, pady=10)

#URL TEXTBOX
url_textbox = tkinter.Entry()
url_textbox.grid(row=1, column=0, sticky="WE", padx = 5, pady= 10)

#DOWNLOAD BUTTON OPTIONS
download_button = tkinter.Button(text="Download", command=button_download_press)
download_button.grid(row=2, column=0, padx=10, pady=10)

#CONSOLE OUTPUT
console_output = ScrolledText()
console_output.grid(row=3, column=0, sticky="WE", padx=10, pady=10)
console_output.configure(state="disabled")


if __name__ == "__main__":
    window.mainloop()



