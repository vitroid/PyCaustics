caustics.mp4: $(wildcard *.png)
	ffmpeg -r 30 -i '%04d.png' -y -pix_fmt yuv420p -vf scale=1280:720 -r 30 $@
