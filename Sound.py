from HelperFunctions import *

class Sound(object):
	def __init__(self, file_path, volume=0.8, frequency=44100, 
				 bitsize=-16, channel=2, buff=2048):
		self.volume = volume
		self.file_path = file_path

	def play(self, checkerFunc=lambda: True):
		mx.init()
		mx.music.set_volume(self.volume)
		try:
			mx.music.load(self.file_path)
		except:
			print(f"The file {self.file_path} can't be loaded")
			return
		mx.music.play()
		while mx.music.get_busy() and checkerFunc():
			continue
		mx.music.stop()

def main():
	inst_sound = Sound("alarmSounds/default.mp3")
	inst_sound.play()

if __name__ == "__main__":
	main()