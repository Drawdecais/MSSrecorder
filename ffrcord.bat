@echo off && chcp 65001>nul
set video_name="video.mp4" && set fps=60 && set sonda=80000k
set thread=700 && set threads=8 && set speaker="Mezcla estéreo (Synaptics HD Audio)"
ffmpeg -loglevel error -stats -f dshow -thread_queue_size %thread% -i audio=%speaker% ^
	-f gdigrab -framerate %fps% -probesize %sonda% -thread_queue_size %thread% -i desktop ^
	-threads %threads% -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 ^
	-c:v libx264 -preset veryfast -crf 0 %video_name% -y
%video_name%