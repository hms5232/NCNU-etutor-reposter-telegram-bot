# NCNU-etutor-reposter-telegram-bot
為[暨大數位學伴計畫](https://www.facebook.com/NCNU.TheProjectofOnlineTutoring/)設計的社團貼文轉貼至 [telegram 頻道](https://t.me/ncnu_etutor_post)的轉貼機器人

## 需求
1. Python 3.7.6 or later
2. pip 套件管理器

## 建立環境 / 部署
※注意！資料夾需要是**可讀寫**的狀態
### 一般方式
※ 如果電腦同時安裝有Python 2 和 3 版本，請使用 pip3 來進行接下來的所有操作
1. 安裝 Python（至少 3.7.6 或更新的版本）
2. 安裝 pip（Linux 請安裝 pip3，例如：`sudo apt install python3-pip`）
3. `pip install python-telegram-bot==12.4.2` 安裝 python-telegram-bot 的 python套件
4. `pip install requests`
5. 複製 config.ini.example 成 config.ini 並填入對應的設定內容
6. 切換至專案目錄底下後，Windows 使用者請執行 `py group_reposter_bot.py.py`或直接點擊 .py 檔案；Linux 使用者請執行 `python3 group_reposter_bot.py`

### 使用 pipenv
1. 安裝 Python（至少 3.7.6 或更新的版本）
2. 安裝 pip（Linux 請安裝 pip3，例如：`sudo apt install python3-pip`）
3. `pip install pipenv`
4. 切換至專案目錄下後執行 `pipenv install`
5. 複製 config.ini.example 成 config.ini 並填入對應的設定內容
5. Windows 使用者請執行 `pipenv run py group_reposter_bot.py`；Linux 使用者請執行 `pipenv run python3 group_reposter_bot.py`

## LICENSE
See [LICENSE](https://github.com/hms5232/NCNU-etutor-reposter-telegram-bot/blob/master/LICENSE).
