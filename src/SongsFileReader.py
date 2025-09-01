# CLASS THAT READS URL INPUTS FROM TXT FILE TO GET URL LIST OF SONGS TO DOWNLOAD

class SongsFileReader:

    def __init__(self, path):
        self.song_url_list = []
        self.transpose_list = []
        with open(path, "r") as songs_to_download_file:
            for url_line in songs_to_download_file:
                url_line = url_line.replace("\n","")
                if("," in url_line): #IF "," IS PRESENT A TRANSPOSE OFFSET IS SPECIFIED
                    url_and_transpose_offset = url_line.split(",") 
                    self.song_url_list.append(url_and_transpose_offset[0])
                    self.transpose_list.append(url_and_transpose_offset[1])
                else: #TRANSPOSE OFFSET NOT SPECIFIED, WE APPEND "0" FOR NO TRANSPOSE
                    if(url_line != ""): #IGNORE EMPTY LINES
                        self.song_url_list.append(url_line)
                        self.transpose_list.append('0')
            self.transpose_list = [int(item) for item in self.transpose_list] #CONVERT FROM STRING TO INT LIST  

    def get_url_list(self):
        return self.song_url_list
    
    def get_transpose_list(self):
        return self.transpose_list