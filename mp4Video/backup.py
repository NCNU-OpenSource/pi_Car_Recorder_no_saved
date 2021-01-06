from glob import glob
import os
def main():
    os.system('python3 rmVideo.py')
    os.chdir('/home/pi/video/1091_LSA_final') 
    os.system('python3 transVideo.py')
    os.chdir('/home/pi/video/1091_LSA_final/mp4Video')
    allDir = glob("*")
    for d in allDir:
        if os.path.isdir(d):
            os.system('rclone copy /home/pi/video/1091_LSA_final/mp4Video/%s/ pi_video:backup/%s' %(d,d))
            
main()

