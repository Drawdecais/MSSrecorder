#https://github.com/Drawdecais/MSSrecorder/blob/main/MSSrecorder.py
import cv2, mss, numpy, pyautogui, keyboard, time, subprocess

fps = 60
images = [] #Array para ingresar las imágenes
size = pyautogui.size() #obtener tamaño del monitor
formato = cv2.VideoWriter_fourcc(*"x264") #formato del vídeo

#video donde se ingresaran las imágenes
video = cv2.VideoWriter('video.mp4', formato, fps, (size.width, size.height))

with mss.mss() as sct:
	#top y left indican la posición donde capturará, width y height el tamaño del capture
	monitor = {"top":0, "left":0, "width": size.width, "height": size.height}
	tiempo = time.time() #Tiempo inicio la grabación
	while True: #inicia un bucle infinito
		cap = sct.grab(monitor) #capture de mss
		img = numpy.array(cap) #convertir en array
		images.append(img) #ingresar en el array
		if keyboard.is_pressed('q'):break #terminar bucle al precionar 'q'

#imprimir el tiempo que duró grabando, este sera el tiempo que debe tener el video final
print("Loanding...","time:",time.localtime(round((time.time()-tiempo),2)).tm_sec)
#convertir todas las imágenes en video
for image in images:video.write(image)
video.release()
"""Este bucle es porque por alguna razon la primera vez que ffmpeg
abre el video da error y la segunda vez si funciona"""
for i in range(3):
	#setpts=2*PTS relentiza en video manteniendo los 60fps
	if subprocess.run(f'ffmpeg -loglevel error -stats -i video.mp4 \
		-filter:v "setpts={fps/28}*PTS" -c:v libx264 -crf 21 -preset slow video2.mp4 -y',
		 shell=True, capture_output=False).returncode == 0:break