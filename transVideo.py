from subprocess import call
from glob import glob

allVideoH = glob("*.h264")
pth = "./mp4Video/"
allVideoM = glob(pth+"*.mp4")
print(allVideoM)
find = 0
for h in allVideoH:
	find = 0
	h = h.replace(".h264","")
	for m in allVideoM:
		m = m.replace("./mp4Video/","")
		m = m.replace(".mp4","")
		if h == m:
			find = 1
			break
	if find == 0:
		command = ("MP4Box -add %s.h264 %s.mp4" %(h, h))
		call([command], shell=True)
		command = ("mv %s.mp4 ./mp4Video" %h)
		call([command], shell=True)
		 
