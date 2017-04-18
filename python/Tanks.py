from urllib.request import urlopen
import os, subprocess

## CHANGE PYTHON PATH HERE ##
path = "C:\Python33\python.exe"

path = os.path.abspath(os.path.join("Tanks.py",os.pardir))
parent = os.path.abspath(os.path.join("Tanks.py",os.pardir)).split("\\").pop()
firstRun = False


if not os.path.exists("Resources"):
    firstRun = True
    os.makedirs("Resources")
    tanks = open("Tanks.bat", 'w')
    contents = """C:\Python33\python.exe Tanks.py"""
    tanks.write(contents)
    tanks.close()
    
try:
    launcher=open("Resources/Launcher.py")
    launcherVersion=launcher.readline()
    launcher.close()
    
    launcherVersion=launcherVersion.replace("# VERSION","")
    launcherVersion=launcherVersion.replace("\n","")
except:
    launcherVersion=0.0
    
webLauncher=urlopen("https://aree-vanier.github.io/python/Launcher.py")
webLauncherContents=webLauncher.read().decode()
webLauncherVersion=webLauncherContents.split("\n")[0]
webLauncherVersion=webLauncherVersion.replace("# VERSION","")
webLauncherVersion=webLauncherVersion.replace("\n","")
print(launcherVersion, webLauncherVersion)
if(float(webLauncherVersion)>float(launcherVersion)):
    Launcher=open("Resources/Launcher.py","w")
    Launcher.write(webLauncherContents)
    Launcher.close()

webLauncher.close()

if(not os.path.basename(__file__) == "Tanks.py"): os.rename(os.path.basename(__file__), "Tanks.py")
subprocess.call(path + " Resources/Launcher.py "+"|"+path+"|")
