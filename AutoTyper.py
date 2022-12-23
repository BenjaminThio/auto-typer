"""Pls do `pip install -r requirements.txt` in terminal"""
import keyboard
import simpleaudio as sa
import threading
import time
import os

delay = 0.01
startKey = 'home'
exitKey = 'escape'
filePath = 'Copy.py'
typingSoundFilePath = 'Sounds/Typing.wav'
endSoundFilePath = 'Sounds/kill.wav'
requireEndSound = False
requireExit = False
requireTimer = True
loop = True

start = False
end = False
file = open(filePath, 'r', encoding='utf8')
lines = file.readlines()
counter = 0
timer = 0
timeCount = True

def IsActive(name):
    if name not in [thread.name for thread in threading.enumerate()]:
        return False
    return True

def Exit():
    global start
    global end
    while True:
        if keyboard.is_pressed(exitKey):
            start = False
            end = True
            break

def Playsound(path):
    wave_object = sa.WaveObject.from_wave_file(path)
    play_object = wave_object.play()
    play_object.wait_done()

def Typing():
    global start
    while start:
        if requireTimer:
            threading.Thread(target=Timer, daemon=True).start()
        for line in lines:
            for char in line:
                if not start:
                    return
                if not IsActive('typing'):
                    threading.Thread(target=Playsound, args=[typingSoundFilePath,], daemon=True, name='typing').start()
                keyboard.write(char)
                time.sleep(delay)
        start = False

def StartTyping():
    global start
    global counter
    global timer
    global timeCount
    pressed = False
    while not start and not end:
        if keyboard.is_pressed(startKey):
            pressed = True
        if pressed and not keyboard.is_pressed(startKey):
            start = True
    Typing()
    if requireEndSound:
        sa.stop_all()
        Playsound(endSoundFilePath)
    sa.stop_all()
    if not end:
        counter += 1
        message = f'Total Task completed: {counter} time'
        if counter > 1:
            message += 's'
        print(f'{message}!')
        if requireTimer:
            message = f'Task completed in {timer} sec'
            if timer > 1:
                message += 's'
            print(f'{message}!')
            timeCount = False

def Timer():
    global timer
    global timeCount
    timer = 0
    timeCount = True
    while timeCount:
        time.sleep(1)
        timer += 1

def main():
    os.system('clear||cls')
    message = f'Click `{startKey}` key to start auto type.'
    if requireExit:
        message = ''.join(list(message)[:-1])
        message += f', click `{exitKey}` to stop auto type.'
    print(message)
    if requireExit:
        threading.Thread(target=Exit, daemon=True).start()
    StartTyping()
    while loop:
        if end:
            break
        StartTyping()

if __name__ == "__main__":
    main()
    print('Task ended!')

"""
*** If you want to use the auto typer in VS Code, pls copy the texts below to settings.json***
    "editor.autoIndent": "none",
    "editor.autoClosingBrackets": "never",
    "editor.acceptSuggestionOnEnter": "off"
"""