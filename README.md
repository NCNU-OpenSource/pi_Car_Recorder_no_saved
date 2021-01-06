# 歡迎使用{ PI 攝者不救 }

## BOT_id
**@CHEN_DASH_bot**

## 需安裝套件
使用前要記得幫您的樹莓派安裝以下套件
- telegram bot
```shell
sudo apt install python3-pip
pip3 install telegram
pip3 install python-telegram-bot
```
- pi camera
```shell
pip3 install picamera
#影片轉檔 .h264轉.mp4
sudo apt install gpac
```
記得要到 `raspi-config` 裡面將 pi camera enable 喔
- rclone (backup to OneDrive)
[git-rclone4pi setup](https://github.com/pageauc/rclone4pi/wiki#manual-install)
- 如果使用Linux server版本，可於筆電反向代理開啟瀏覽器，授權OneDrive帳號
```shell=
ssh -L 53682:127.0.0.1:53682 [user name]@[your ip]
# ex: 
ssh -L 53682:127.0.0.1:53682 pi@192.168.1.60
```
- 在`/home/pi`下建立 `start.sh` 
```shell=
cd /home/pi
vim start.sh
```
```shell=
# 備份前先移除一周前的影片
cd /home/pi/video/1091_LSA_final/mp4Video
python3 rmVideo.py
# 影片轉檔
cd /home/pi/video/1091_LSA_final
python3 transVideo.py
# 備份mp4Video的影片至OneDrive
cd /home/pi
rclone copy /home/pi/video/1091_LSA_final/mp4Video pi_video:backup
```
- crontab:  每分鐘執行`/home/pi/`下的`start.sh`檔案，將結果記錄到`logfile`中
```shell=
crontab -e
*/1 * * * * sh /home/pi/start.sh 2>&1 > /home/pi/logfile
```

## BOT_command
- `start`
  - 開始操作
- `about`
  - 關於PI攝者不救
- `start`
  - 開始操作 
- `record`
  - 開始錄影
- `end`
  - 停止錄影
- `get`
  - 取得影片雲端連結
- `search`
  - 從本地搜尋特定影片
- `backup`
  - 手動備份
- `help`
  - 如何使用
