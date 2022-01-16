
import PySimpleGUI as sg
import threading
import time
import sys
import os

import subprocess

def run(cmd):
    output = subprocess.check_output("powershell.exe "+cmd, stderr=subprocess.STDOUT, shell=True)
    return output

if len(sys.argv) < 2 or len(sys.argv) > 3 :
    print("---->")
    print("Usage: python main2.py filname1 filename2  (last filename is obtional)")
    print()
    os._exit(0)


two_argv = (len(sys.argv) == 3)    
    
fileName1 = sys.argv[1]  
if two_argv:
    fileName2 = sys.argv[2]
    with open(fileName2) as f:
        for line in (f.readlines() [-1:]):
            lastline2 = line
        
    with open(fileName2) as f:        
        for line in (f.readlines() [-2:-1]):
            secondlastline2 = line

with open(fileName1) as f:
    for line in (f.readlines() [-1:]):
        lastline1 = line
        
with open(fileName1) as f:        
    for line in (f.readlines() [-2:-1]):
        secondlastline1 = line



backupFileAge1 = int(run('$1 = (Get-Item {}).CreationTime; $2 = get-date; ($2-$1).Days'.format(fileName1)))
accessedLastDays1 = int(run('$1 = (Get-Item {}).LastWriteTime; $2 = get-date; ($2-$1).Days'.format(fileName1)))
if two_argv:
    backupFileAge2 = int(run('$1 = (Get-Item {}).CreationTime; $2 = get-date; ($2-$1).Days'.format(fileName2)))
    accessedLastDays2 = int(run('$1 = (Get-Item {}).LastWriteTime; $2 = get-date; ($2-$1).Days'.format(fileName2)))



def countdown_close():
    time.sleep(10)
    stopped = True
    os._exit(0)
    
def delete_file(filename):
    if os.path.exists(filename):
        if os.path.exists(filename+"bak"):
            os.remove(filename+".bak")
        os.rename(filename, filename+".bak")
    window['Delete1'].update(visible=False)  
    threading.Thread(target=countdown_close, args=(), daemon=True).start()

    
    

sg.theme('Black')


messageOK = "Din backup ser ud til at køre normalt"
messageDelFile = "Log-fil er mere end 14 dage gammel"
messageNotOK = "Backup kører ikke - kald på Lars"

colorOK = 'lightgreen'
colorNotOK = 'Red'
colorDelete = 'Orange'



# This block for something wrong
if accessedLastDays1 > 5:
    message1 = messageNotOK
    myTextColor1 = colorNotOK  
    canbeseen1 = False

# This block for Log-file is old and needs deleting

elif backupFileAge1 >= 14 and accessedLastDays1 < 5:
    message1 = messageDelFile
    myTextColor1 = colorDelete
    canbeseen1 = True


# This block for everytihing is OK

elif backupFileAge1 < 14 and accessedLastDays1 < 5:
    message1 = messageOK
    myTextColor1 = colorOK   
    canbeseen1 = False
    threading.Thread(target=countdown_close, args=(), daemon=True).start()




layout1 = [
    [sg.Text('Information om '+fileName1, size=(20, 1), font=("Times New Roman", 30), text_color='LightBlue')],
    
    [sg.Text('', size=(2, 1)), sg.Text(message1, size=(27, 1), font=("Times New Roman",25),text_color=myTextColor1, key='-MAIN-')],
    [sg.Text('', size=(10, 1)), sg.Text(secondlastline1, size=(30, 1), font=("Times New Roman",12),text_color='white', key='second')],
    [sg.Text('', size=(10, 1)), sg.Text(lastline1, size=(30, 1), font=("Times New Roman",12),text_color='white', key='last')],  
    [sg.Button('Slet log-fil', size=(10,2), visible=canbeseen1, button_color=('Black', 'Orange'), key='Delete1' ),
    sg.Button('Luk', size=(10,2), button_color=('white', 'Red'), key='Exit')]
]

layout2 = [
    [sg.Text('Information om '+fileName1, size=(20, 1), font=("Times New Roman", 30), text_color='LightBlue')],
    
    [sg.Text('', size=(2, 1)), sg.Text(message1, size=(27, 1), font=("Times New Roman",25),text_color=myTextColor1, key='-MAIN-')],
    [sg.Text('', size=(10, 1)), sg.Text(secondlastline1, size=(30, 1), font=("Times New Roman",12),text_color='white', key='second')],
    [sg.Text('', size=(10, 1)), sg.Text(lastline1, size=(30, 1), font=("Times New Roman",12),text_color='white', key='last')],  
    [sg.Text('', size=(10, 1)), sg.Text(secondlastline2, size=(30, 1), font=("Times New Roman",12),text_color='white', key='second')],
    [sg.Text('', size=(10, 1)), sg.Text(lastline2, size=(30, 1), font=("Times New Roman",12),text_color='white', key='last')],  
    
    [sg.Button('Slet log-fil', size=(10,2), visible=canbeseen1, button_color=('Black', 'Orange'), key='Delete1' ),
    sg.Button('Luk', size=(10,2), button_color=('white', 'Red'), key='Exit')]
]

if two_argv:
    window = sg.Window('DIT BACKUP TJEK', layout2)
else:
    window = sg.Window('DIT BACKUP TJEK', layout1)
    
if __name__ == '__main__':

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
            break
        if event == 'Delete1':
            delete_file(fileName1)
            if two_argv:
                delete_file(fileName2)


    window.close()
