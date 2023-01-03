from pygame import mixer


class Music():

    def __init__(self):
        self.path = None
        self.soundplay = None
        print("DUpa")

    def music_play(self, musicpath):
        if musicpath == 1:
            self.path = "./../sounds/elevator.wav"
        elif musicpath == 2:
            self.path = "./../sounds/tokyo.wav"

        mixer.music.load(self.path)  # muzyka
        mixer.music.play(-1)

    def sound_play(self, soundpath):
        self.soundplay = mixer.Sound(soundpath)
        self.soundplay.play()
