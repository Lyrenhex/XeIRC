import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import os
import sys
import random
import time
import _thread as thread
import easygui

print("""
    XeIRC IRC Client  Copyright (C) 2016  Damian Heaton
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
""")

pre = []
if os.path.exists("details.txt") and os.access("details.txt", os.R_OK):
    for line in open("details.txt").read().split("\n"):
        if line != "":
            pre.append(line)

details = easygui.multpasswordbox("Enter IRC Connection Details.", "Connect to IRC.", ["Nickname", "Server", "Port",
                                                                                       "Channel", "Password"],
                                  pre)

f = open("details.txt", "w")
f.write("")
f.close()
f = open("details.txt", "a")
for line in details:
    f.write(line+"\n")
f.close()

botnick = details[0]
server = details[1]
port = int(details[2])
if details[4] == "":
    nickserv = False
else:
    nickserv = True
password = details[4]
global primary
primary = [details[3]]
secondary = []
global channel
channel = details[3]

#ctypes.windll.kernel32.SetConsoleTitleW("XeIRC - "+botnick+" @ "+server+":"+str(port))

if os.path.isdir("logs") == False:
    os.mkdir("logs")
if os.path.isdir("logs/"+botnick) == False:
    os.mkdir("logs/"+botnick)
if os.path.isdir("logs/"+botnick+"/"+server) == False:
    os.mkdir("logs/"+botnick+"/"+server)
logdir = "logs/"+botnick+"/"+server

msgs = []

global irc
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to: "+server)
irc.connect((server,port))
irc.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+ botnick +"\n", "utf-8"))
irc.send(bytes("NICK "+ botnick +"\n", "utf-8"))

text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
    
if nickserv:
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
print("i")
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
    
root = tk.Tk()
root.title("XeIRC IRC Client")
frame = tk.Frame(root)
frame.pack(fill='both', expand='yes')

chatLog = ScrolledText(
    master = frame,
    wrap   = 'word',  # wrap text at full words only
    width  = 25,      # characters
    height = 10,      # text lines
    bg = 'black',        # background color of edit area
    fg = 'white'
)
# the padx/pady space will form a frame
chatLog.pack(fill='both', expand=True)
chat = tk.Text(frame, padx=4, height=1)
chat.pack(fill='x')
chatLog.config(state="disabled")
def addchat(text):
    chatLog.config(state="normal")
    chatLog.insert("insert", text + "\n")
    chatLog.see(tk.END)
    chatLog.config(state="disabled")
def enterPressed(event):
    channel = primary[0]
    #addchat(chat.get("1.0",'end-1c'))
    sendt = chat.get("1.0",'end-2c')
    try:
        pars = sendt.split(" ")
    except:
        pars = [sendt]
    chat.delete("1.0",'end')
    print(sendt)
    if "@" in sendt:
        msgid = sendt.split("|")[0].split("@")[1]
        sendt = "\x1d"+msgs[int(msgid)]+"\x1d | " + sendt.split("|")[1]
    if pars[0] == "/chan":
        channel = sendt.split(" ")[1]
    elif pars[0] == "/showchan":
        addchat("Currently chatting on " + channel)
    elif pars[0] == "/join":
        channel = sendt.split(" ")[1]
        irc.send(bytes("JOIN "+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
    elif pars[0] == "/quit":
        irc.send(bytes("QUIT :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
    elif pars[0] == "/names":
        irc.send(bytes("NAMES :"+ channel +"\n", "utf-8"))
    elif pars[0] == "/away":
        irc.send(bytes("AWAY :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
        irc.send(bytes("NICK :"+ botnick +"^away\n", "utf-8"))
    elif pars[0] == "/back":
        irc.send(bytes("AWAY\n", "utf-8"))
        irc.send(bytes("NICK :"+ botnick +"\n", "utf-8"))
    elif pars[0] == "/invite":
        irc.send(bytes("INVITE :"+ sendt.split(" ", 1)[1] + " " + sendt.split(" ", 2)[2] +"\n", "utf-8"))
    elif pars[0] == "/kick":
        irc.send(bytes("PRIVMSG ChanServ :kick "+ channel +" "+ sendt.split(" ", 1)[1] + " " + sendt.split(" ",
                                                                                                           2)
        [2] + "\n", "utf-8"))
    elif pars[0] == "/help":
        addchat("Help:")
        addchat("@<messageid>|<text> will quote the message at that messageid")
        addchat("/showchan will show the current channel talking on")
        addchat("/chan <channel/nick> will switch the chatting channel to to <channel/nick>. \
Ensure that you have joined the channel, if trying to chat on a channel, first")
        addchat("/join <channel> [password] will join the channel for listening and /chan'ing to to speak")
        addchat("/quit <message> will quit the server")
        addchat("/away <message> will set you as away (and change your nickname accordingly)")
        addchat("/back will un-set you as away (and change your nick back)")
        addchat("/invite <nick> <channel> will invite <nick> to <channel>")
        addchat("/kick <nick> will kick <nick> from the current channel")
        addchat("/names will list the people on the current channel")
    elif sendt == "":
        pass
    else:
        irc.send(bytes("PRIVMSG "+ channel +" :" + sendt + "\n", "utf-8"))
        msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+channel+"] <"+botnick+"> "+sendt
        msgs.append(msg)
        addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
root.bind('<Return>', enterPressed)

def getMsgs():
    while True:
        text = str(irc.recv(2040))
        unraw=text.split("\\r\\n")
        for line in unraw:
            print(line)
            try:
                chan = line.split(" :")[0].split(" ")[2]
                nick = line.split(":")[1].split("!")[0]
                text = line.split(":", 2)[2]
                pars = text.lower().split(" ")
            except:
                nick = "Service"
                chan = "unknown channel"
            if server in nick:
                nick = "Service"
            try:
                if nick != "Service":
                    msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] <"+nick+"> "+text
                    if '\\x0' in msg:
                        msg = msg.replace("\\x0f", "[normal]")
                        msg = msg.replace("\\x0310", "[turquoise]")
                        msg = msg.replace("\\x031", "[black]")
                        msg = msg.replace("\\x032", "[blue]")
                        msg = msg.replace("\\x033", "[green]")
                        msg = msg.replace("\\x034", "[red]")
                        msg = msg.replace("\\x035", "[brown]")
                        msg = msg.replace("\\x036", "[purple]")
                        msg = msg.replace("\\x037", "[orange]")
                        msg = msg.replace("\\x038", "[yellow]")
                        msg = msg.replace("\\x039", "[light green]")
                        msg = msg.replace("\\x030", "[white]")
                    msgs.append(msg)
                    addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
                    file = open(logdir+"/"+chan+".log", "a")
                    file.write("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)] + "\n")
                    file.close()
                    if botnick in text:
                        print("\a", end="")
            except Exception as e:
                print(e)
            if line.find("PING :") != -1 and nick == "Service":
                irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
            elif line.find("JOIN :") != -1:
                for chan1 in primary:
                    irc.send(bytes("JOIN "+ chan1 +"\n", "utf-8"))
                for chan1 in secondary:
                    irc.send(bytes("JOIN "+ chan1 +"\n", "utf-8"))
                if nick != botnick:
                    msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] * "+ line.split(":")[1].split("!")[0] \
                          +" has joined " + line.split(":")[2] + "."
                    msgs.append(msg)
                    addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
            elif line.find("PART :") != -1:
                if nick != botnick:
                    msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                          +" has left the channel: "+line.split(":", 2)[2]+"."
                    msgs.append(msg)
                    addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
            elif line.find("QUIT :") != -1:
                if nick != botnick:
                    msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                          +" has left the server: "+line.split(":", 2)[2]+"."
                    msgs.append(msg)
                    addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
            elif line.find("NICK :") != -1:
                if nick != botnick:
                    msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                        +" has changed their name: "+line.split(":", 2)[2]+"."
                    msgs.append(msg)
                    addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
            elif line.find("353") != -1:
                addchat("*** People currently on channel: "+text + "\n")
thread.start_new_thread(getMsgs, ())
        
root.mainloop()
