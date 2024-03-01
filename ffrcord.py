import subprocess, sys
video_name="video.mp4";fps=60;thread=sys.argv[1];threads=8
def cmd(comand):subprocess.run(comand, shell=True)
cmd(f'ffmpeg -loglevel error -stats -f dshow -thread_queue_size {thread} -i \
    audio="Mezcla estéreo (Synaptics HD Audio)" -f gdigrab -framerate {fps} \
	-probesize 80000k -thread_queue_size {thread} -i desktop -threads {threads}\
	-pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
	-c:v libx264 -preset veryfast -crf 0 {video_name} -y')

