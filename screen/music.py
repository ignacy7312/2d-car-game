from pygame import mixer


class Music():

    def __init__(self):
        print("DUpa")

    def music_play(self, musicpath):
        mixer.music.load(musicpath)  # muzyka
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)

    def sound_play(self,vol, soundpath):
        self.soundplay = mixer.Sound(soundpath)
        mixer.Sound.set_volume(self.soundplay, vol)
        self.soundplay.play()
