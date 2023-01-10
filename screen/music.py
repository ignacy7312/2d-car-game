from pygame import mixer
from db import storagedriver

class Music():

    def __init__(self):
        self.storge_driver = storagedriver.StorageDriver()
        self.play_sounds = self.storge_driver.get_sounds()
        self.playing = False
        
    def music_play(self, musicpath):
        if self.play_sounds:
            self.playing = True
            mixer.music.load(musicpath)  # muzyka
            mixer.music.set_volume(0.4)
            mixer.music.play(-1)


    def sound_play(self,vol, soundpath):
        if self.play_sounds:
            self.soundplay = mixer.Sound(soundpath)
            mixer.Sound.set_volume(self.soundplay, vol)
            self.soundplay.play()

    def keep_playing(self):
        self.play_sounds = self.storge_driver.get_sounds()
        if not self.play_sounds:
            mixer.music.pause()
        elif self.playing:
            mixer.music.unpause()
        else:
            return True