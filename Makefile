caustics.mp4:
	ffmpeg -r 30 -i '%04d.png' -y -pix_fmt yuv420p -r 30 $@
