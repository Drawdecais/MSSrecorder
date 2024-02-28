#https://github.com/Drawdecais/MSSrecorder
import cv2, mss, numpy, pyautogui, keyboard, time

images = [] #Array para ingresar las imágenes
tiempo = time.time() #Tiempo inicio del programa
size = pyautogui.size() #obtener tamaño del monitor
formato = cv2.VideoWriter_fourcc(*'h264') #formato del vídeo

#video donde se ingresaran las imágenes
video = cv2.VideoWriter('video.mp4', formato, 25, (size.width, size.height))


with mss.mss() as sct:
	#top y left indican la posición donde capturará
	#width y height el tamaño del capture
	monitor = {"top":0, "left":0, "width": size.width, "height": size.height}
	#inicia un bucle infinito
	while True:
		cap = sct.grab(monitor) #capture de mss
		img = numpy.array(cap) #convertir en array
		images.append(img) #ingresar en el array
		if keyboard.is_pressed('q'):break #terminar bucle al precionar 'q'

#convertir todas las imágenes en video
for image in images:video.write(image)
video.release()
#imprimir el tiempo que duró grabando
print(time.localtime(round((time.time() - tiempo),2)).tm_sec)