#
# Serial COM Port terminal program
# 2022/07/19, John

import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import serial_rx_tx
import _thread

import os
import time


# globals
serialPort = serial_rx_tx.SerialPort()

root = tk.Tk()  # create a Tk root window
root.title("GUI For Serial Data Terminal")
# set up the window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/2 + 70

window_height = screen_width/3
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))
SavingPath = os.getcwd()
savingStatus = ""

# scrolled text box used to display the serial data
frame = tk.Frame(root, bg='cyan')
# frame.pack(side="bottom", fill='both', expand='no')
frame.pack(side="bottom", fill='both', expand=0)
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=28)  # width=characters, height=lines
textbox.pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

# COM Port label
label_comport = Label(root, width=10, height=2, text="COM Port:")
label_comport.place(x=10, y=26)
label_comport.config(font="bold")

# Path Label
label_path = Label(root, width=10, height=2, text="Path:")
label_path.place(x=420, y=30)
label_path.config(font="bold")

# period Label
label_period = Label(root, width=10, height=2, text="Period:")
label_period.place(x=190, y=115)
label_period_unit = Label(root, width=10, height=2, text="ms")
label_period_unit.place(x=260, y=115)

# Baud Rate label
label_baud = Label(root,width=10,height=2,text="Baud Rate:")
label_baud.place(x=10,y=70)
label_baud.config(font="bold")

#
# data entry labels and entry boxes
#


# Period entry box
period_edit = Entry(root, width=5)
period_edit.place(x=250, y=125)
period_edit.insert(END, "200")

# COM Port entry box
comport_edit = Entry(root, width=10)
comport_edit.place(x=100, y=36)
comport_edit.config(font="bold")
comport_edit.insert(END, "COM9")

# Saving Path editbox
saving_path_edit = Entry(root, width=55)
saving_path_edit.place(x=450, y=70)
saving_path_edit.insert(END, SavingPath)

# Baud Rate entry box
baudrate_edit = Entry(root,width=10)
baudrate_edit.place(x=100,y=80)
baudrate_edit.config(font="bold")
baudrate_edit.insert(END,"115200")

# Send Data entry box
senddata_edit = Entry(root,width=30)
senddata_edit.place(x=210,y=155)
senddata_edit.config(font="bold")
senddata_edit.insert(END,"Message")


def saveConsecutiveData(message):
    filename = time.strftime('%Y%m%d')
    f = open(SavingPath+"/"+filename+"-consecutive.txt", "a")
    timestamp = time.strftime("%H:%M:%S\t")
    f.write(timestamp+message)
    f.close()


def saveSingleData(message):
    filename = time.strftime('%Y%m%d')
    f = open(SavingPath+"/"+filename+"-single.txt", "a")
    timestamp = time.strftime("%H:%M:%S\t")
    f.write(timestamp+message)

    f.close()

# serial data callback function
def OnReceiveSerialData(message):
    str_message = message.decode("utf-8")
    textbox.insert('1.0', str_message)
    if savingStatus == "saveOnce":
        saveSingleData(str_message)
    elif savingStatus == "saveCyclic":
        saveConsecutiveData(str_message)

# Register the callback above with the serial port object
# serialPort.RegisterReceiveCallback(OnReceiveSerialData)


def sdterm_main():
    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#
#  commands associated with button presses
#


def OpenCommand():
    if button_openclose.cget("text") == 'Open COM Port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        serialPort.Open(comport,baudrate)
        # Register the callback above with the serial port object
        serialPort.RegisterReceiveCallback(OnReceiveSerialData)

        button_openclose.config(text='Close COM Port')
        textbox.insert('1.0', "COM Port Opened\r\n")
    elif button_openclose.cget("text") == 'Close COM Port':
        serialPort.Close()
        button_openclose.config(text='Open COM Port')
        textbox.insert('1.0',"COM Port Closed\r\n")


def ClearDataCommand():
    textbox.delete('1.0',END)


def cyclic_sending(t, message):
    while(button_senddata.cget("text")=="STOP"):
        if serialPort.IsOpen():
            message += '\r\n'
            serialPort.Send(message)
        time.sleep(t/1000.0)


def SendDataCommand():
    message = senddata_edit.get()

    if savingStatus == "saveCyclic" and button_senddata.cget("text") == "Send" and serialPort.IsOpen():
        button_senddata.config(text='STOP')
        _thread.start_new_thread(cyclic_sending, (int(period_edit.get()), message+'\r\n'))

    elif savingStatus == "saveCyclic" and button_senddata.cget("text") == "STOP" and serialPort.IsOpen():
        button_senddata.config(text='Send')

    else:
        if serialPort.IsOpen():
            message += '\r\n'
            serialPort.Send(message)
            textbox.insert('1.0', message)
        else:
            textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample1():
    if serialPort.IsOpen():
        msg = '--Command1--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample2():
    if serialPort.IsOpen():
        msg = '--Command2--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample3():
    if serialPort.IsOpen():
        msg = '--Command3--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample4():
    if serialPort.IsOpen():
        msg = '--Command4--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample5():
    if serialPort.IsOpen():
        msg = '--Command5--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def SendingExample6():
    if serialPort.IsOpen():
        msg = '--Command6--\r\n'
        serialPort.Send(msg)
        textbox.insert('1.0', msg)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")


def OpenSavingPath():
    global SavingPath, saving_path_edit
    root.filename = filedialog.askdirectory(initialdir="/", title="Select Saving Dir")
    SavingPath = root.filename
    saving_path_edit.delete(0, END)
    saving_path_edit.insert(0, SavingPath)


# COM Port open/close button
button_openclose = Button(root,text="Open COM Port",width=20,command=OpenCommand)
button_openclose.config(font="bold")
button_openclose.place(x=210,y=30)

# Clear Rx Data button
button_cleardata = Button(root,text="Clear Rx Data",width=20,command=ClearDataCommand)
button_cleardata.config(font="bold")
button_cleardata.place(x=210,y=72)

# Send Message button
button_senddata = Button(root,text="Send",width=5,command=SendDataCommand)
button_senddata.config(font="bold")
button_senddata.place(x=470,y=150)

# saving file path
button_savingPath = Button(root, text="Search", width=6, command=OpenSavingPath)
button_savingPath.config(font="bold")
button_savingPath.place(x=490, y=35)


def radio1_func():
    # period setting ,  saving path setting
    radio_status('disabled', 'normal', "saveOnce")


def radio2_func():
    radio_status('normal', 'normal', "saveCyclic")


def radio3_func():
    radio_status('disabled', 'disabled', "nonSave")


def radio_status(state1, state2, status):
    global period_edit, saving_path_edit, savingStatus
    period_edit.config(state=state1)
    saving_path_edit.config(state=state2)
    savingStatus = status


saving_radio = tk.IntVar()
saving_radio.set(1)
radio1_func()
button_saving1 = tk.Radiobutton(root, text="Saving a Single Response",
                                value=1, variable=saving_radio, command=radio1_func)
button_saving1.place(x=20, y=120)

button_saving2 = tk.Radiobutton(root, text="Saving Cyclical Response",
                                value=2, variable=saving_radio, command=radio2_func)
button_saving2.place(x=20, y=140)

button_saving3 = tk.Radiobutton(root, text="Non-Saving",
                                value=3, variable=saving_radio, command=radio3_func)
button_saving3.place(x=20, y=160)

# button_saving1.pack()
# button_saving2.pack()


# Example Function1
button_tutorials1 = Button(root,text="Command1",width=12,command=SendingExample1)
button_tutorials1.config(font="bold")
button_tutorials1.place(x=600, y=105)

# Example Function2
button_tutorials2 = Button(root,text="Command2",width=12,command=SendingExample2)
button_tutorials2.config(font="bold")
button_tutorials2.place(x=730, y=105)

# Example Function3
button_tutorials3 = Button(root,text="Command3",width=12,command=SendingExample3)
button_tutorials3.config(font="bold")
button_tutorials3.place(x=860, y=105)

# Example Function4
button_tutorials4 = Button(root,text="Command4",width=12,command=SendingExample4)
button_tutorials4.config(font="bold")
button_tutorials4.place(x=600, y=145)

# Example Function5
button_tutorials5 = Button(root,text="Command5",width=12,command=SendingExample5)
button_tutorials5.config(font="bold")
button_tutorials5.place(x=730, y=145)

# Example Function6
button_tutorials6 = Button(root,text="Command6",width=12,command=SendingExample6)
button_tutorials6.config(font="bold")
button_tutorials6.place(x=860, y=145)


#
# The main loop
#

root.after(200, sdterm_main)
root.mainloop()