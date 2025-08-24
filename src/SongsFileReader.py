# CLASS THAT READS URL INPUTS FROM TXT FILE TO GET URL LIST OF SONGS TO DOWNLOAD

class SongsFileReader:

    def __init__(self, path):
        self.song_url_list = []
        with open(path, "r") as songs_to_download_file:
            for url_line in songs_to_download_file:
                url_line = url_line.replace("\n","")
                self.song_url_list.append(url_line)

    def get_url_list(self):
        return self.song_url_list