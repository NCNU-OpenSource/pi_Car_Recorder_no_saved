import os
from glob import glob
import datetime
def main():
    all_video= glob("*.mp4")
    now = datetime.datetime.now()
    seven_days_ago=now-datetime.timedelta(days=7)
    seven_days_ago = seven_days_ago.strftime("%Y%m%d%H%M%S")
    for i in range(len(all_video)):
        if all_video[i].split(".mp4")[0] <= seven_days_ago:
            os.system('rm %s' %(all_video[i]))
            os.system('rm ../%s' %(all_video[i].split(".mp4")[0]+".h264"))
main()

