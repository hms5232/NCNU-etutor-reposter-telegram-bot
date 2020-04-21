@echo off
@echo Before run this batch, please sure your computer has installed git.
@echo You can visit the following tutorial to install Git for Windows:
@echo     https://github.com/doggy8088/Learn-Git-in-30-days/blob/master/zh-tw/02.md
@echo:
IF EXIST "%cd%\.git" (
@echo on
git checkout master
git pull
) ELSE (
@echo Git repo not found!
)
@echo:
@pause
