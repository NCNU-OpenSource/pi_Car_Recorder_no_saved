import os
from glob import glob
import datetime
def main():
    all_dir = glob("*")
    for d in all_dir:
        if os.path.isdir(d):
            rm_old_video(d)
    print("remove directly")
def rm_old_video(d): 
    os.chdir('/home/pi/video/1091_LSA_final/mp4Video/%s' %(d))
    all_video= glob("*.mp4")
    now = datetime.datetime.now()
    seven_days_ago=now-datetime.timedelta(days=7)
    seven_days_ago = seven_days_ago.strftime("%Y%m%d%H%M")
    for i in range(len(all_video)):
        os.popen('ls')
        if all_video[i].split(".mp4")[0] <= seven_days_ago:
            os.system('rm %s' %(all_video[i]))

main()

