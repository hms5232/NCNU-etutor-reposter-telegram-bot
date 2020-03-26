#!/usr/bin/env python3

"""
Author：hms5232
Repo：https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot
Bug：https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot/issues
"""


from telegram.ext import Updater, CommandHandler
from configparser import ConfigParser
import requests


# 設定一些個人的環境變數
env = ConfigParser()
env.read('config.ini')
# If you don't want use config.ini, please edit following variables for your environment.
telegram_bot_token = env.get('reposter', 'telegram_bot_token')
fb_token = env['reposter']['fb_token']
fb_group_id = env['reposter']['fb_group_id']


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
	
	update.message.reply_text(user_info)


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


# CommandHandler('指令', 要執行的函數)，使用者輸入「/指令」
updater.dispatcher.add_handler(CommandHandler(['start', 'about'], welcome))  # 歡迎訊息 / 機器人資訊
updater.dispatcher.add_handler(CommandHandler('info', show_user_info))  # 顯示使用者資訊
#updater.dispatcher.add_handler(CommandHandler('post', post))  # TODO: 發公告
updater.dispatcher.add_handler(CommandHandler('latest', show_latest_posts))  # 顯示最新幾篇貼文
updater.dispatcher.add_handler(CommandHandler(['hello', 'hi'], hello))  # Hello World!
updater.dispatcher.add_handler(CommandHandler('reload', reload_config))  # 重新讀取設定檔


# 執行機器人必須要的，讓機器人運作聽命
updater.start_polling()
updater.idle()
