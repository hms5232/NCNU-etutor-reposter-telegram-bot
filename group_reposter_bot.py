#!/usr/bin/env python3

"""
Author：hms5232
Repo：https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot
Bug：https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot/issues
"""


from telegram.ext import Updater, CommandHandler
from configparser import ConfigParser
import requests
import time
import threading


# 設定一些個人的環境變數
env = ConfigParser()
env.read('config.ini')
# If you don't want use config.ini, please edit following variables for your environment.
telegram_bot_token = env.get('reposter', 'telegram_bot_token')
fb_token = env['reposter']['fb_token']
fb_group_id = env['reposter']['fb_group_id']


listen_status = True  # 機器人是否監聽新貼文的狀態


"""
	尚未執行機器人之前，可傳送訊息給機器人後至下列網址查看：
	
		https://api.telegram.org/bot{$token}/getUpdates
"""
updater = Updater(token=telegram_bot_token)  # 呼叫 bot 用


"""
	對應指令的函數們
	
	@param bot: 機器人預設值一定要，如果沒有給的話，你的機器人不會回覆
	@param update: Telegram update資訊
"""
# 歡迎訊息
def welcome(bot, update):
	chat_id = update.message.from_user.id
	
	about_bot = ''
	about_bot = about_bot + '本機器人由 [hms5232](https://github.com/hms5232) 開發\n'
	about_bot = about_bot + '採用 [Apache許可證](https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot/blob/master/LICENSE)\n'
	about_bot = about_bot + '原始碼公開於 [Github](https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot)\n'
	about_bot = about_bot + 'bug 回報及建議請[往這裡走](https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot/issues)'
	
	bot.send_message(chat_id, about_bot, parse_mode='Markdown')


# 顯示使用者資訊
def show_user_info(bot, update):
	user_info = ''
	user_info = user_info + '發送人 first name：{}\n'.format(update.message.from_user.first_name)
	user_info = user_info + '發送人 last name：{}\n'.format(update.message.from_user.last_name)
	user_info = user_info + '發送人 full name：{}\n'.format(update.message.from_user.full_name)
	user_info = user_info + '發送人 username：{}\n'.format(update.message.from_user.username)
	user_info = user_info + '發送人 id：{}\n'.format(update.message.from_user.id)
	user_info = user_info + 'message_id：{}\n'.format(update.message.message_id)
	user_info = user_info + '所在的聊天室 id：{}\n'.format(update.message.chat.id)
	user_info = user_info + '所在的聊天室 type：{}\n'.format(update.message.chat.type)
	user_info = user_info + '訊息內容：{}\n'.format(update.message.text)
	
	update.message.reply_text(user_info, disable_notification="True")


# TODO: 顯示最新幾篇貼文的資訊
def show_latest_posts(bot, update):
	# https://www.facebook.com/groups/{社團ID}/permalink/{貼文ID}/
	pass


def hello(bot, update):
	# 兩種方法傳送訊息予使用者
	update.message.reply_text('Hello world!')  #方法一
	bot.sendMessage(update.message.from_user.id, 'Welcome to Telegram!')  # 方法二
	"""
		方法二的 sendMessage 是 send_message 的別名
		以 python 的使用習慣，應該是後者較為符合
		https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.send_message
	"""


# 更新設定檔
def reload_config(bot, update):
	# 先檢查是不是 telegram 管理員
	if not is_telegram_admin(update.message.from_user.id):
		# 不是管理員更新個X
		# TODO: 發通知到群組？
		update.message.reply_text('Permission denied!')
		return
	
	new_env = ConfigParser()
	new_env.read('config.ini')

	global telegram_bot_token, fb_token, fb_group_id

	telegram_bot_token = new_env.get('reposter', 'telegram_bot_token')
	fb_token = new_env['reposter']['fb_token']
	fb_group_id = new_env['reposter']['fb_group_id']

	update.message.reply_text('OK, config updated!')


# 確認使用者是否為指定的 telegram 管理員
def is_telegram_admin(telegram_user_id):
	telegram_user_id = str(telegram_user_id)  # 當前使用者 user id
	env = ConfigParser()
	env.read('config.ini')
	telegram_admins = [str_val for str_val in env['reposter']['telegram_admin_id'].split(',')]
	return telegram_user_id in telegram_admins


# 監聽社團
def listen():
	print('thread')
	failed_request_times = 0
	while True:
		if listen_status:
			r = requests.get('https://graph.facebook.com/{}/feed?fields=admin_creator,created_time,id,message,message_tags,permalink_url,link,from&access_token={}'.format(fb_group_id, fb_token))
			if r.status_code == 200:  # OK
				failed_request_times = 0  # 重設歸零
				# TODO: 分析內容並轉貼
				pass
			else:
				failed_request_times += 1
				
				# 失敗超過一定次數就停止
				if failed_request_times >= 5:
					# TODO: 通知大家
					print("Attempt failed too many times!")
					return
			time.sleep(30)
		else:
			return


# 叫機器人起來工作了
def start_work(bot, update):
	# 先檢查是不是 telegram 管理員
	if not is_telegram_admin(update.message.from_user.id):
		# 不是管理員用個X
		# TODO: 發通知到群組？
		update.message.reply_text('Permission denied!')
		return
	
	global listen_status, listen_group
	listen_status = True
	listen_group = threading.Thread(target = listen)  # 重新設定執行緒
	if listen_status:
		listen_group.start()  # 開新執行緒
		# 確認執行緒是不是真的開啟了
		if listen_group.is_alive():
			update.message.reply_text('OK, I go to work now QQ.')
		else:
			update.message.reply_text('Oh no, something went wrong.')
	else:
		update.message.reply_text('Oh no, something went wrong.')


# 機器人可以下班休息下囉，可是還是要待命（慣老闆語氣）
def unlisten(bot, update):
	# 先檢查是不是 telegram 管理員
	if not is_telegram_admin(update.message.from_user.id):
		# 不是管理員用個X
		# TODO: 發通知到群組？
		update.message.reply_text('Permission denied!')
		return
	
	print("stop thread")
	global listen_status, listen_group
	listen_status = False
	listen_group.join()  # 關閉執行緒
	print("thread killed")
	listen_group = threading.Thread(target = listen)  # 重新設定執行緒
	if not listen_status and not listen_group.is_alive():
		update.message.reply_text('OK, now I get off work. YA~!')
	else:
		update.message.reply_text('Oh no, something went wrong.')


# 看看 bot 是否正在監聽社團貼文
def bot_work_status(bot, update):
	now_status = ''
	if listen_group.is_alive():
		now_status = now_status + 'ξ( ✿＞◡❛)▄︻▇▇〓▄︻┻┳═一監聽社團貼文中\n'
	else:
		now_status = now_status + '現在是手動模式(:3[__]4\n'

	update.message.reply_text(now_status)


# CommandHandler('指令', 要執行的函數)，使用者輸入「/指令」
updater.dispatcher.add_handler(CommandHandler(['start', 'about'], welcome))  # 歡迎訊息 / 機器人資訊
updater.dispatcher.add_handler(CommandHandler('info', show_user_info))  # 顯示使用者資訊
#updater.dispatcher.add_handler(CommandHandler('post', post))  # TODO: 發公告
updater.dispatcher.add_handler(CommandHandler('latest', show_latest_posts))  # 顯示最新幾篇貼文
updater.dispatcher.add_handler(CommandHandler(['hello', 'hi'], hello))  # Hello World!
updater.dispatcher.add_handler(CommandHandler('reload', reload_config))  # 重新讀取設定檔
updater.dispatcher.add_handler(CommandHandler('work', start_work))  # 開始社畜生活囉
updater.dispatcher.add_handler(CommandHandler('rest', unlisten))  # 可以下班了
updater.dispatcher.add_handler(CommandHandler('status', bot_work_status))  # 看看現在 bot 有在認真看貼文嗎


listen_group = threading.Thread(target = listen)  # 採用多執行緒來監聽


# 執行機器人必須要的，讓機器人運作聽命
updater.start_polling()
updater.idle()
