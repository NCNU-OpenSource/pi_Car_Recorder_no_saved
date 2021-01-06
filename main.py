#-*- coding: UTF-8 -*-
from telegram import ParseMode
import time
import json
import os
import os.path
import logging
import telegram
import picamera
import datetime as dt
from time import sleep
from subprocess import call
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import threading

# 允許 logging。當出現error時能知道哪裡出了問題。
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

flag = False

# 創造Updater，將token pass給Updater。
# 在v12中要加入“use_context = True”（之後版本不需要），用於有新訊息是回應。
# TOKEN、bot和updater要放在def外面。若只放在main()會出現錯誤
TOKEN = "1499587189:AAGtXXGIVnPekHxSjBpZmp4voDUc_Fl7h6Q"
bot = telegram.Bot(token = TOKEN)
updater = Updater(TOKEN, use_context = True)
dp = updater.dispatcher
uid = None
def run():
    global flag
    global uid
    with picamera.PiCamera() as camera:
        while(1):
            #if flag == True:
            #   camera.stop_recording()
                  #  return
            startTime = dt.datetime.now().strftime('%Y%m%d%H%M')
            camera.rotation = 180
            camera.start_preview()
            camera.annotate_background = picamera.Color('black')  
            camera.annotate_text = dt.datetime.now().strftime('%Y%-m%-d %H:%M:%S')
            camera.start_recording("%s%s.h264"%(uid ,startTime))
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < 5:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.2)
                if flag == True:
                    camera.stop_recording()
                    return
            camera.stop_recording()
         #command = ("MP4Box -add %s.h264 %s.mp4" %(startTime, startTime))
         #call([command], shell=True) 

def do_backup():
    os.system('python3 rmVideo.py')
    os.chdir('/home/pi/video/1091_LSA_final')
    os.system('python3 transVideo.py')
    os.system('rclone copy /home/pi/video/1091_LSA_final/mp4Video pi_video:backup')
    return

def start_handler(update, context: CallbackContext):
    # reply_markup = ReplyKeyboardMarkup([[
    #     KeyboardButton("/about"),
    #     KeyboardButton("/help")],
    #     [KeyboardButton("/start")]])
    # bot.sendMessage(chat_id=-1, text='選項如下:', reply_markup=reply_markup)
    # chatbot在接受用戶輸入/start後的output內容
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING) # 會顯示chatbot正在輸入中，增加對話真實感
    time.sleep(0.5) # 在顯示輸入中後停頓1秒，然後顯示下一句code的文字
    update.message.reply_text("Hello! 你好👋，{}！我是PI攝者不救🤖".format(update.message.from_user.first_name)) # 給user的output
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("PI攝者不救🤖能根據關鍵字執行行車記錄器內容\n\n❓關於指令使用方法，請輸入 /help \n💬關於PI攝者不救🤖，或想要報錯和反饋💭，請輸入 /about") # 給user的output。output可以分開多次使用update.message.reply_text()。
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton("/about"), KeyboardButton("/backup")]
        , [KeyboardButton("/record"), KeyboardButton("/end")]
        , [KeyboardButton("/get"), KeyboardButton("/help")]])
    bot.sendMessage(chat_id=update.message.chat_id, text="指令如下", reply_markup=reply_markup)


def help_handler(update, context: CallbackContext):

    # chatbot在接受用戶輸入/start後的output內容
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("《🔍如何使用》\n若要開始拍攝\n輸入：「/record」\n若要停止拍攝\n輸入：「/end」\n關於PI攝者不救🤖️，或想要報錯和反饋💭\n輸入：「/about」") 

def about_handler(update, context: CallbackContext):

    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("感謝使用PI攝者不救🤖️。\n這是一個行車記錄器的BOT，可以控制開始與關閉錄影，也可以取得影片檔案的雲端連結。") 
    # bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    # time.sleep(1)
    # update.message.reply_text("徐長卿君🤖️儲存的資料很多，所有資料都是主人親手校對整理，出錯在所難免，因此若想要報錯，又或者有任何疑問、建議，或者想透過徐長卿君🤖️宣傳、洽談合作，可以去扶疏堂研究所的Facebook page私訊聯繫，或者歡迎瀏覽扶疏堂研究所的網站看看其他項目和服務。")
    
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("點我前往", url = "https://www.facebook.com/profile.php?id=100003827470832")]])
    #     InlineKeyboardButton("Facebook", url = "https://www.facebook.com/herboratory/ "),
    #     InlineKeyboardButton("Website", url = "https://herboratory.ai/")],
    #     InlineKeyboardButton("關於徐長卿君🤖️ About Cynanchum kun🤖️", callback_data="about_me")]])

    bot.send_message(update.message.chat.id, "若要回報錯誤，透過以下連結Facebook私訊林科左回報。", reply_to_message_id = update.message.message_id,
                     reply_markup = reply_markup)

    # chatbot在接受用戶輸入/start後的output內容

# def addOnedrive_handler(update, context: CallbackContext) :

# 開始拍攝
def Record_handler(update, context: CallbackContext) :
    global uid 
    uid = update.message.from_user.username
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("開始拍攝！")
    global flag
    flag = False
    t1 = threading.Thread(target = run) 
    t1.start()
    # t1.join()

# 停止拍攝
def End_handler(update, context: CallbackContext) :
    global flag
    flag = True
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("停止拍攝，影片已儲存至雲端。")

# 取得影片雲端連結
def getVideo_handler(update, context: CallbackContext) :
    time.sleep(0.5)
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("點我前往", url = "https://onedrive.live.com/?authkey=%21AKanIMwDpSXJ3Qw&id=3FF58B5EF46ED07A%211886&cid=3FF58B5EF46ED07A")]])

    bot.send_message(update.message.chat.id, "行車記錄器檔案", reply_to_message_id = update.message.message_id,
                     reply_markup = reply_markup)
# def test(update, context: CallbackContext) :
#     bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
#     time.sleep(0.5)
#     update.message.reply_text(update.)
#查詢檔案名稱
def Search_handler(update, context: CallbackContext) :
#    T = update.message.text.split(" ")
    # bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    # time.sleep(0.5)
 #   update.message.reply_text(T[1])
#    bot.send_video(chat_id = update.message.chat_id, video = open('mp4Video/' + T[1] + '.mp4', 'rb'))

    # reply_markup = InlineKeyboardMarkup([[
    #     InlineKeyboardButton("點我取得檔案名稱", callback_data="about_me")]])
    # #     InlineKeyboardButton("Facebook", url = "https://www.facebook.com/herboratory/ "),
    # #     InlineKeyboardButton("Website", url = "https://herboratory.ai/")],
    # #     InlineKeyboardButton("關於徐長卿君🤖️ About Cynanchum kun🤖️", callback_data="about_me")]])

    # bot.send_message(update.message.chat.id, "按下面連結查看檔案", reply_to_message_id = update.message.message_id,
    #                  reply_markup = reply_markup)


    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    result = os.system('ls mp4Video/ | grep .mp4 > record.txt')
    data = ""
    with open("record.txt", "r") as f:
        for line in f:
            data += "<pre>" +line + "</pre>"
    os.system("rm record.txt")
    bot.send_message(update.message.chat.id, data , parse_mode=ParseMode.HTML)


# def getClickButtonData(update, context):
#     """
#     透過上方的about function取得了callback_data="about_me"，針對取得的參數值去判斷說要回覆給使用者什麼訊息
#     取得到對應的callback_data後，去判斷說是否有符合，有符合就執行 update.callback_query.edit_message_text
#     傳送你想傳送的訊息給使用者
#     由於這裡不再是單純發訊息，而是再用callback_query的方法，發訊息時，chat_id = update.message.chat_id是不能用，要改成chat_id = update.callback_query.message.chat_id
#     而
#     而偽裝輸入正在輸入中也要改成chat_id = update.callback_query.message.chat_id
#     """
    
#     if update.callback_query.data == "about_me":
#         bot.send_chat_action(chat_id = update.callback_query.message.chat_id, action = telegram.ChatAction.TYPING)
#         time.sleep(1)
#         result = os.system('ls > record.txt')
#         data = ""
#         with open("record.txt", "r") as f:
#             for line in f:
#                 data += line
#         os.system("rm record.txt")
#         update.callback_query.edit_message_text(data)
#         # dp.add_handler(MessageHandler(Filters.text, search2))


def backup_handler(update, context: CallbackContext):
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("備份中...")
    do_backup()
    update.message.reply_text("備份完成!")

def reply_handler(update, context: CallbackContext):
    """Reply message."""
    text = update.message.text
    LEN = len(text)
    MP4 = text[LEN-4:LEN:+1]
    if (MP4 == ".mp4") :
        bot.send_video(chat_id = update.message.chat_id, video = open('mp4Video/' + text, 'rb'))
    # if (text == "/start") or (text == "/about") or (text == "/record") or (text == "/end") or (text == "/get") or (text == "/search") or (text == "/backup") or (text == "/help") :
    #     return
    else :
        bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
        time.sleep(0.5)
        update.message.reply_text("對不起，PI攝者不救🤖不能理解你說啥。🤔\n\n關於指令使用方法，請輸入 /help \n💬關於PI攝者不救🤖️，或想要報錯和反饋💭的聯繫方式，請輸入 /about")
     

def error_handler(bot, update, error, context: CallbackContext):
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("對不起，PI攝者不救🤖不能理解你說啥。🤔\n\n關於指令使用方法，請輸入 /help \n💬關於PI攝者不救🤖️，或想要報錯和反饋💭的聯繫方式，請輸入 /about")

def error(update, context):
    """紀錄Updates時出現的errors。出現error時console就會print出下面logger.warning的內容"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """啟動bot"""
# ...
    # 設定使用dispatcher，用來以後設定command和回覆用

    dp.add_handler(CommandHandler("start", start_handler)) # 啟動chatbot
#    dp.add_handler(CommandHandler("add", addOnedrive_handler)) # 新增Onedrive網址
    dp.add_handler(CommandHandler("record", Record_handler)) # 開始拍攝
    dp.add_handler(CommandHandler("end", End_handler)) # 停止拍攝
    dp.add_handler(CommandHandler("get", getVideo_handler)) # 取得影片雲端連結
    dp.add_handler(CommandHandler("search", Search_handler)) # 搜尋本地影片
    dp.add_handler(CommandHandler("help", help_handler)) # 顯示幫助的command
    dp.add_handler(CommandHandler("about", about_handler)) # 顯示關於PI攝者不救🤖️的command
    dp.add_handler(CommandHandler("backup", backup_handler)) # 手動備份檔案
#    dp.add_handler(CallbackQueryHandler(getClickButtonData)) # 設定關於徐長卿君🤖️的按鈕連結
    dp.add_handler(MessageHandler(Filters.text, reply_handler)) # 設定若非設定command會回覆用戶不知道說啥的訊息
    dp.add_error_handler(error_handler) # 出現任何非以上能預設的error時會回覆用戶的訊息內容

    # 專門紀錄所有errors的handler，對應def error()
    dp.add_error_handler(error)

    # 啟動Bot。bot程式與Telegram連結有兩種方式：polling和webhook。
    # 兩者的差異可以參考這篇reddit的解釋：https://www.reddit.com/r/TelegramBots/comments/525s40/q_polling_vs_webhook/。
    # 在python-telegram-bot裡面本身有built-in的webhook方法，但是在GCE中暫時還沒摸索到如何設定webhook，因此polling是最便捷的方法。
    updater.start_polling()
    
    # 就是讓程式一直跑。
    # 按照package的說法“start_polling() is non-blocking and will stop the bot gracefully.”。
    # 若要停止按Ctrl-C 就好
    updater.idle()

#運行main()，就會啟動bot。
if __name__ == '__main__':
    main()


#    update.message.reply_text(update.message.from_user.username) 
