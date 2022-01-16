# hello_psg.py

import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# Create the window
window = sg.Window("Demo", layout)

stop = 2

print(stop)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if stop == 2:
        exit()
    stop = stop - 1
    print(stop)
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    

window.close()