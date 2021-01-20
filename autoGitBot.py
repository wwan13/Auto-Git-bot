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
    print("cd {}\n".format(currentPath))
    os.chdir("uploadedFiles")

@sleepPerUnit
def backToRootDir():
    currentPath = os.getcwd()
    os.chdir("..")


def getDateTimeStr():
    currentDateTime = datetime.now()
    datetimeFormat = currentDateTime.strftime("%y%m%d-%p%I%M%S")
    return datetimeFormat


@sleepPerUnit
def makeNewFile():
    fileName = format(getDateTimeStr() + ".py")
    os.system("touch " + fileName)
    print("create >> " + fileName + "\n")


@sleepPerUnit
def gitAddCommitPush():
    print("$ git add .\n")
    os.system("git add .")
    print("\n$ git commit -m \"{}\"\n".format(getDateTimeStr()))
    os.system("git commit -m \"{}\"".format(getDateTimeStr()))
    print("\n$ git push origin master\n")  
    os.system("git push origin master")
    print("\nupload complete")


def autoGitUploade():
    accessWorkingDir()
    makeNewFile()
    gitAddCommitPush()
    backToRootDir()

schedule.every(10).minutes.do(autoGitUploade)
# schedule.every().day.at("16:12").do(autoGitUploade)

while True:
    schedule.run_pending()
    sleep(1)

