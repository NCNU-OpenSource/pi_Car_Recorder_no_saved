from subprocess import call
from glob import glob
from time import time
def checkDir(uid):
    alldir = glob("./mp4Video/"+"*")
    for a in alldir:
        if a == uid:
            return True
    return False

allVideoH = glob("*.h264")
uid=""
day=""
fullName=""
for h in allVideoH:
    h = h.replace(".h264","")
    fullName = h
    h = h.split("@")
    uid = h[0]
    day = h[1]
    command = ("MP4Box -add %s.h264 %s.mp4" %(fullName, day))
    call([command], shell=True)
    if checkDir(uid) == False:
        command = ("mkdir ./mp4Video/%s" % uid)
        call([command], shell=True)
    command = ("mv %s.mp4 ./mp4Video/%s" %(day,uid))
    call([command], shell=True)
    command = ("rm %s.h264" %fullName)
    call([command], shell=True)

		 
