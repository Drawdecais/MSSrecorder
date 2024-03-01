import cv2, mss, numpy, pyautogui, keyboard, time, subprocess, soundcard as sc, soundfile as sf, threading
from moviepy.editor import VideoFileClip, AudioFileClip
class runGrabar():
	def __init__(self,nombre_video,nombre_audio,video_end,fps):
		speakers = sc.all_speakers();self.Grabar=True
		if len(speakers) == 1:speaker = sc.default_speaker().name
		else:
			for i, speaker in enumerate(speakers):print(i, speaker.name)
			x = int(input('Enter device:'));speaker = str(speakers[x].id)
		self.sem = threading.Semaphore(2)
		A = threading.Thread(target=self.GrabarAudio,args=(nombre_audio,speaker,));A.start()
		V = threading.Thread(target=self.GrabarVideo,args=(nombre_video,fps,));V.start()
		while self.Grabar:
			if keyboard.is_pressed('0'):self.Grabar = False;A.join();V.join()
		self.ffmpeg(nombre_video,nombre_audio,video_end)
	def GrabarAudio(self,nombre_audio,speaker):
		with sc.get_microphone(id=speaker,include_loopback=True).recorder(samplerate=44100) as mic:
			with sf.SoundFile(nombre_audio, mode='w', samplerate=44100, channels=2, subtype='PCM_16') as audio:
				self.sem.acquire()
				while self.Grabar:audio.write(mic.record(numframes=44100))
				self.sem.release()
	def GrabarVideo(self,nombre_video,fps):
		size = pyautogui.size()
		with mss.mss() as sct:
			video = cv2.VideoWriter(nombre_video, cv2.VideoWriter_fourcc(*'x264'), fps, (size.width,size.height))
			monitor = {"top":0,"left":0,"width":size.width,"height":size.height}
			self.sem.acquire();tiempo=time.time()
			while self.Grabar:video.write(numpy.array(sct.grab(monitor)))
			self.sem.release();video.release();self.time_end=time.time()-tiempo
	def ffmpeg(self,nombre_video,nombre_audio,video_end):
		video_time = VideoFileClip(nombre_video).duration
		pts = max(self.time_end,video_time) / min(self.time_end,video_time)
		subprocess.run(f'ffmpeg -loglevel error -stats -i {nombre_video} -i {nombre_audio} \
			-map 0:v -map 1:a -filter:v "setpts={pts}*PTS" -c:v libx264 -crf 21 -preset veryfast -60\
			{video_end} -y', shell=True)
		print("time_end",self.time_end,"video_time:",video_time)
		print("PTS",round(pts,2),"  time_end:",time.localtime(self.time_end).tm_min,":",time.localtime(self.time_end).tm_sec)
runGrabar('video.mp4','audio.flac','video-end.mp4',30)