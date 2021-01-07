# 歡迎使用{ PI 攝者不救 }

## BOT_id
**@CHEN_DASH_bot**

## BOT_command
- `start`
  - 開始操作
- `about`
  - 關於PI攝者不救
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
  
## 設定telegram bot
- 套件 
```shell
# 用於 main.py
sudo apt install python3-pip
pip3 install telegram
pip3 install python-telegram-bot
```

### 設定 pi camera 
- 套件 
```shell
# 用於 main.py
pip3 install picamera
#影片轉檔 .h264轉.mp4 (用於 transVideo.py)
sudo apt install gpac
```
- 到 `raspi-config` 裡面將 pi camera enable 
```
sudo raspi-config
選 inter face option
選 camera
```
```
由於本次實驗 pi camera 是反著插入固定 camera 的地方，因此將錄影在輸出時轉動 180 度。
若 camera 為正著放，可以刪除 main.py 的第 42 行(camera.rotation = 180)
```
### 設定 雲端備份
- rclone (backup to OneDrive)
[git-rclone4pi setup](https://github.com/pageauc/rclone4pi/wiki#manual-install)
- 如果使用Linux server版本，可於筆電輸入以下開啟瀏覽器，授權OneDrive帳號
```shell=
ssh -L 53682:127.0.0.1:53682 [user name]@[your ip]
# ex: 
ssh -L 53682:127.0.0.1:53682 pi@192.168.1.60
```
- 在`/home/pi`下建立 `start.sh` 
```shell=
cd /home/pi
vim start.sh
# 執行備份
cd /home/pi/video/1091_LSA_final/mp4Video
# 執行了rmVideo.py, transVideo.py
python3 backup.py
```
- crontab:  每分鐘執行`/home/pi/`下的`start.sh`檔案，將結果記錄到`logfile`中
```shell=
crontab -e
*/1 * * * * sh /home/pi/start.sh 2>&1 > /home/pi/logfile
```
### 把 `main.py` 加入 service (在背景執行)
- 注意: 這邊我們將`main.py`放在 `/home/pi/video/1091_LSA_final/`下
```
cd /etc/systemd/system
sudo vim pi_video.service
sudo systemctl enable pi_video.service
sudo systemctl daemon-reload
sudo systemctl start pi_video.service
```
- `pi_video.service` 內容 
  - Description: `sudo systemctl status pi_video.service`會顯示的內容
  - ExecStart: 要在背景執行的程式(絕對路徑下)
  - WorkingDirectory: 在背景執行的程式所在目錄(絕對路徑下)
```
[Unit]
Description=Shut up and take my video!!
After=network.target

[Service]
ExecStart=/usr/bin/nohup /usr/bin/python3 /home/pi/video/1091_LSA_final/main.py &
WorkingDirectory=/home/pi/video/1091_LSA_final/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

## 工作分配
- pi camera & 轉影片 : 蔣毓庭(主要)
- 雲端備分 & 零零碎碎的工作 : 謝芝瑜(主要)
- telegram bot : 林科佑 張宸瑜(主要)
- 題目討論 & ppt & readMe & 抓蟲子 & 找資料 : 大家 
