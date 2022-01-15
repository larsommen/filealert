
import PySimpleGUI as sg
import threading
import time
import sys
import os

import subprocess

def run(cmd):
    output = subprocess.check_output("powershell.exe "+cmd, stderr=subprocess.STDOUT, shell=True)
    return output
    
fileName = sys.argv[1]  


with open(fileName) as f:
    for line in (f.readlines() [-1:]):
        lastline = line
        
with open(fileName) as f:        
    for line in (f.readlines() [-2:-1]):
        secondlastline = line


#def lastAccessed(filename):
#    return run('$1 = (Get-Item .\test.log).LastWriteTime; $2 = get-date; ($2-$1).Days')

#def created(filename):
#    return run('$1 = (Get-Item .\test.log).CreationTime; $2 = get-date; ($2-$1).Days')




backupFileAge = int(run('$1 = (Get-Item {}).CreationTime; $2 = get-date; ($2-$1).Days'.format(fileName)))
accessedLastDays = int(run('$1 = (Get-Item {}).LastWriteTime; $2 = get-date; ($2-$1).Days'.format(fileName)))



def countdown_close():
    time.sleep(10)
    stopped = True
    os._exit(0)
    
def delete_file(filename):
    if os.path.exists(filename):
        if os.path.exists(filename+"bak"):
            os.remove(filename+".bak")
        os.rename(filename, filename+".bak")
    window['Delete'].update(visible=False)     

    
    

sg.theme('Black')


messageOK = "Din backup ser ud til at køre normalt"
messageDelFile = "Log-fil er mere end 14 dage gammel"
messageNotOK = "Backup kører ikke - kald på Lars"

colorOK = 'lightgreen'
colorNotOK = 'Red'
colorDelete = 'Orange'



# This block for something wrong
if accessedLastDays > 5:
    message = messageNotOK
    myTextColor = colorNotOK  
    canbeseen = False

# This block for Log-file is old and needs deleting

elif backupFileAge >= 14 and accessedLastDays < 5:
    message = messageDelFile
    myTextColor = colorDelete
    canbeseen = True


# This block for everytihing is OK

else:
    message = messageOK
    myTextColor = colorOK   
    canbeseen = False
    threading.Thread(target=countdown_close, args=(), daemon=True).start()




layout = [
    [sg.Text('Information om din backup ', size=(20, 1), font=("Times New Roman", 30), text_color='LightBlue')],
    
    [sg.Text('', size=(2, 1)), sg.Text(message, size=(27, 1), font=("Times New Roman",25),text_color=myTextColor, key='-MAIN-')],
    [sg.Text('', size=(10, 1)), sg.Text(secondlastline, size=(30, 1), font=("Times New Roman",12),text_color='white', key='second')],
    [sg.Text('', size=(10, 1)), sg.Text(lastline, size=(30, 1), font=("Times New Roman",12),text_color='white', key='last')],  
    [sg.Button('Slet log-fil', size=(10,2), visible=canbeseen, button_color=('Black', 'Orange'), key='Delete' ),
    sg.Button('Luk', size=(10,2), button_color=('white', 'Red'), key='Exit')]
]
window = sg.Window('DIT BACKUP TJEK', layout)

if __name__ == '__main__':

    while True:
        if sys.argv[1] == "10":
            print("Jeg er her")
            threading.Thread(target=countdown_close, args=(), daemon=True).start()

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):        # ALWAYS give a way out of program
            break
        if event == 'Delete':
            delete_file(fileName)


    window.close()
