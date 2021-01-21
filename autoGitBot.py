import os
from time import sleep
from datetime import datetime
import schedule


def sleepPerUnit(func):
    def wrapper():
        sleep(0.3)
        func()
    return wrapper


@sleepPerUnit
def accessWorkingDir():
    currentPath = os.getcwd()
    print("$ cd {}\n".format(currentPath))
    os.chdir("uploadedFiles")


@sleepPerUnit
def backToRootDir():
    currentPath = os.getcwd()
    print("$ cd ..\n")
    os.chdir("..")


def getDateTimeStr():
    currentDateTime = datetime.now()
    datetimeFormat = currentDateTime.strftime("%y%m%d-%p%I%M%S")
    return datetimeFormat


@sleepPerUnit
def makeNewFile():
    fileName = format(getDateTimeStr() + ".py")
    print("$ touch " + fileName + "\n")
    os.system("touch " + fileName)


@sleepPerUnit
def gitAddCommitPush():
    COMMAND_LIST = [
        "git add .",
        "git commit -m \"{}\"".format(getDateTimeStr()),
        "git push origin master"
    ]

    for COMMAND in COMMAND_LIST:
        print("\n$ " + COMMAND + "\n")
        os.system(COMMAND)

    print("\n-- {} UPLOAD COMPLETE --\n".format(datetime.now()))


def autoGitUploade():
    accessWorkingDir()
    makeNewFile()
    backToRootDir()
    gitAddCommitPush()


def uploadEveryNoon():
    schedule.every().day.at("12:00").do(autoGitUploade)

    while True:
        schedule.run_pending()
        sleep(1)


def uploadEveryAppointedMinute(minute):
    schedule.every(minute).minutes.do(autoGitUploade)

    while True:
        schedule.run_pending()
        sleep(1)


# autoGitUploade()
uploadEveryNoon()
# uploadEveryAppointedMinute(1)

