import PySimpleGUI as sg
import threading
import time
import sys
import os


def thread_reminder(seconds, window):
    count = 0
    while count < seconds :
        count += 1
        time.sleep(1)
        print(count)
    window.write_event_value('Alarm', "1 minute passed")
if sys.argv[1] == "10":
    besked = "Alt er OK og jeg lukker selv ned"
    tekst_farve= 'lightgreen'
    canbeseen = False
else:
    besked = "Din log-fil er for gammel og børe slettes"
    tekst_farve= 'Red'
    canbeseen = True
    


layout = [
    [sg.Text('', size=(20, 1))],
    
    [sg.Text('', size=(10, 2)), sg.Text(besked, size=(55, 18), font=("Times New Roman",16),text_color=tekst_farve, key='-MAIN-')],
  
    [sg.Button('Slet log-fil', size=(10,2), visible=canbeseen )],
]
window = sg.Window('APP', layout)

stopped = False

def countdown_close():
    print("Starts sleeping")
    time.sleep(10)
    stopped = True
    print("Stopper nu")
    os._exit(0)


while True:
    print(sys.argv[1])
    if sys.argv[1] == "10":
        print("Jeg er her")
        threading.Thread(target=countdown_close, args=(), daemon=True).start()
    
    event, values = window.read()
    
            
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Start':
        threading.Thread(target=thread_reminder, args=(10, window), daemon=True).start()
    elif event == 'Alarm':
        message = values[event]
        sg.popup_auto_close(message)
    
window.close()

