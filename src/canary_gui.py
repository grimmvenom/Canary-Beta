"""
Summary:
    Python Script to run webform via a webservice to run as the GUI of the Ivan Application

Author:
    grimmvenom <grimmvenom@gmail.com>


Helpful CSS Tool:
https://github.com/uncss/uncss

"""

import os
import sys
import platform
import eel
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog
import subprocess


@eel.expose
def file_picker():
    try:
        root = Tk()
        root.attributes("-topmost", True)
        root.update()
        # root.withdraw()
        filepath = filedialog.askopenfilename()
        root.withdraw()
        return filepath
    except:
        pass
   

@eel.expose
def run_canary(args):
    print("\n")
    print(args)
    print("\n\n")
    urls = list()
    for index, data in enumerate(args):
        try:
            args[index] = data.replace("'", '')
        except:
            pass
    command = [str(sys.executable) + " " + str(current_dir) + os.sep + "main.py"]
    if args[0].split("\n"):  # url_text
        for url in args[0].split("\n"):
            command.append('-u ' + str(url) + '')
    if args[1]:  # url_file
        command.append('-f ' + str(args[1]) + '')
    if args[2]:  # type
        command.append('-' + str(args[2]))
    if args[3]:  # enable_excel
        command.append('--excel')
    if args[4]:  # Enable Advanced options
        if args[5]:  # base_url_enable
            if args[6]:  # base_url
                command.append('-base ' + str(args[6]))
        if args[7]:  # limit_domain_enable
            if args[8]:  # limit_domain
                command.append('--limit ' + str(args[8]))
        if args[9]:  # exclude_domain_enable
            if args[10]:  # exclude_domain
                command.append('--exclude ' + str(args[10]))
        if args[11]:  # auth_enable
            if args[12] and args[13]:  # Username and Password
                command.append('--user ' + str(args[12]))
                command.append('--password ' + str(args[13]))
        if args[14]:  # database_enable
            if args[15]:  # database
                command.append('--db ' + str(args[15]))
                if args[16]:  # execute_automation
                    command.append("--execute")
    print(" ".join(command))
    
    if platform.system() == "Windows":
        # print("Running on Windows")
        execute_windows(" ".join(command))
    elif platform.system() == "Darwin":
        # print("Running on Mac")
        execute_mac(" ".join(command))
    elif platform.system() == "Linux":
        execute_linux(" ".join(command))
    else:
        print("Could Not Detect Operating System")
        pass


def execute_windows(command):
    terminal_emulator = 'start cmd /k \"COMMAND\"'
    new = terminal_emulator.replace("COMMAND", command)
    os.popen(new)
    
    
def execute_mac(command):
    # osascript - e 'tell app "Terminal" to do script "python3 main.py -b \"Chrome\" -s \"/Users/user/Scripts/BitBucket/Perficient/Ivan/ply_dev/ivan_examples/AllCommandTest.txt\""'
    terminal_emulator = "osascript -e "
    terminal_emulator = terminal_emulator + "'tell app \"Terminal\" to do script \"COMMAND\"'"

    new = terminal_emulator.replace("COMMAND", command)
    
    print("\n", new)
    os.popen(new)


def execute_linux(command):
    terminal_emulators = {
        'gnome-terminal': "gnome-terminal -- /bin/bash -c 'COMMAND'",  # {'gnome-terminal': 'subprocess.call(["gnome-terminal", "-x bash" ,"-c ", "export PATH=$PATH:/opt/selenium;" + COMMAND])',
        'konsole': 'konsole --hold -e /bin/bash -c "COMMANDL"',  # 'konsole': '["konsole","--hold", "-e", "/bin/bash -c PATH=$PATH:/opt/selenium && str(Command_to_Run)"]',
        'xterm': 'xterm -hold -T Ivan -e "COMMAND"'}  # 'xterm': 'subprocess.call(["xterm", "-hold", "-T", "Ivan", "-e", "export PATH=$PATH:/opt/selenium && " + str(Command_to_Run) + " && $SHELL"])'}

    found = False
    while found is False:
        for emulator in terminal_emulators:
            found = check_existence(emulator)
            if found is True:
                terminal_emulator = terminal_emulators[emulator]
                # new = terminal_emulator.replace("COMMAND", command)
                
                print("\n", command)
                subprocess.call(command, shell=True)
                # os.popen(new)
                # Process = terminal_emulators[emulator]
                # Process = Process.replace("COMMAND", str(Command))
                # print(str(Process))x
                # os.system(Process)
                # subprocess.call(Process)
                # exec(terminal_emulators[emulator])
                print(" ")
                break
            else:
                terminal_emulator = "Not Found"


def check_existence(application):
    found = False
    rc = subprocess.call(['which', application])
    if rc == 0:
        found = True
        print(application + ' installed!')
    else:
        found = False
    # print(application + ' not found!')
    return found


if __name__ == "__main__":
    print("Running Canary GUI")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    init_dir = current_dir + os.sep + 'app' + os.sep + 'resources' + os.sep + 'web_template'
    
    
    eel.init(init_dir)
    web_app_options = {
            'mode': "chrome",  # or "chrome-app"
            'host': 'localhost',
            'port': 8080,
            'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
    }
    try:
        eel.start('index.html', size=(1000, 1000), options=web_app_options)
    except Exception as e:
        print(e)
        print("Attempting to Open Using Firefox")
        try:
            web_app_options['mode'] = "firefox"
            eel.start('index.html', size=(1000, 1000), options=web_app_options)
        except Exception as e:
            print(e)
            pass
        pass
