import os
def main():
    os.system('python3 rmVideo.py')
    os.chdir('/home/pi/video/1091_LSA_final') 
    os.system('python3 transVideo.py')
    os.system('rclone copy /home/pi/video/1091_LSA_final/mp4Video pi_video:backup')
main()

