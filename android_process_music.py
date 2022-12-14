import eyed3
import os, shutil
import mutagen
from mutagen.mp4 import MP4
from mutagen.id3 import APIC, ID3
import re
eyed3.log.setLevel("ERROR")
print("Current working directory: {0}".format(os.getcwd()))
music_folder="to process"
to_output_to="output"
class process:
    def __init__(self):
        if not os.path.exists(music_folder):
            os.mkdir(music_folder)
        self.music_list=self.load_mp3s()
        print("loading", self.music_list)
        self.remove_artwork()

    def load_mp3s(self):
        return [os.path.join(music_folder, path) for path in os.listdir(os.path.join(os.getcwd(), music_folder))]

    def remove_artwork(self):
        for audio in self.music_list:
            if audio.endswith(".mp3") or audio.endswith(".aac"):
                mp3 = ID3(audio)
                mp3.delall("APIC")
                mp3.save()
                process.sort_folders(mp3, audio, mp3['TPE1'].text[0])
            elif audio.endswith(".m4a"):
                process.sort_folders(mp3, audio, MP4(audio).tags["©ART"][0])
            
    @staticmethod
    def sort_folders(mp3, audio_location, artist_name=None):
        if artist_name is None:
            artist_name=mp3.tag.artist
        #artist_name=artist_name.replace(":"," ")
        artist_name=re.sub("[:|\\|\/|\*|\"|<|>|\|]", "",artist_name)
        print(artist_name)
        where_to_output=os.path.join(to_output_to, artist_name)
        if not os.path.exists(where_to_output):
            os.makedirs(where_to_output)
        shutil.move(audio_location, os.path.join(where_to_output, os.path.basename(audio_location)))
        
        
process()
