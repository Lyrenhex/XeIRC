# -*- coding: utf-8 -*-

"""
    XeIRC Python IRC Client with native NickServ support
    Copyright (C) 2015  Adonis Megalos

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# colours
# [56] [2015.09.19 21:43:49] [#8bit] <Scratso^logs> XeIRC notes: \x031black \x032blue \x033green \x034red \x035brown \x036purple \x037orange \x038yellow \x039lightgreen \x0310teal/turquoise-y? \x030white

import socket
import os
import sys
import random
import time
import _thread as thread
import easygui
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("XeIRC")

print("""
    XeIRC IRC Client  Copyright (C) 2015  Adonis Megalos
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
""")

pre = []
if os.path.exists("details.txt") and os.access("details.txt", os.R_OK):
    for line in open("details.txt").read().split("\n"):
        if line != "":
            pre.append(line)
# pre = ["Scratso", "irc.editingarchive.com", "6667", "#8bit", "damianos2008"]

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
primary = [details[3]]
secondary = []

ctypes.windll.kernel32.SetConsoleTitleW("XeIRC - "+botnick+" @ "+server+":"+str(port))

if os.path.isdir("logs") == False:
    os.mkdir("logs")
if os.path.isdir("logs/"+botnick) == False:
    os.mkdir("logs/"+botnick)
if os.path.isdir("logs/"+botnick+"/"+server) == False:
    os.mkdir("logs/"+botnick+"/"+server)
logdir = "logs/"+botnick+"/"+server

msgs = []

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to: "+server)
irc.connect((server,port))
irc.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+ botnick +"\n", "utf-8"))
irc.send(bytes("NICK "+ botnick +"\n", "utf-8"))

text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    #print(line)
    try:
        nick = line.split(":")[1].split("!")[0]
        text = line.split(":", 2)[2]
    except:
        nick = "Service"
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))

if nickserv:
    irc.send(bytes("PRIVMSG NickServ :IDENTIFY damianos2008\n", "utf-8"))

def send():
    channel = "#8bit"
    while True:
        try:
            sendt = easygui.enterbox(channel, "Send IRC Message")
            if sendt is None:
                sendt = ""
            if "@" in sendt:
                msgid = sendt.split("|")[0].split("@")[1]
                sendt = "\x1d"+msgs[int(msgid)]+"\x1d | " + sendt.split("|")[1]
            if "/chan" in sendt:
                channel = sendt.split(" ")[1]
            elif "/join" in sendt:
                channel = sendt.split(" ")[1]
                irc.send(bytes("JOIN "+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
            elif "/quit" in sendt:
                irc.send(bytes("QUIT :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
            elif "/names" in sendt:
                irc.send(bytes("NAMES :"+ channel +"\n", "utf-8"))
            elif "/away" in sendt:
                irc.send(bytes("AWAY :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
                irc.send(bytes("NICK :"+ botnick +"^away\n", "utf-8"))
            elif "/back" in sendt:
                irc.send(bytes("AWAY\n", "utf-8"))
                irc.send(bytes("NICK :"+ botnick +"\n", "utf-8"))
            elif "/invite" in sendt:
                irc.send(bytes("INVITE :"+ sendt.split(" ", 1)[1] + " " + sendt.split(" ", 2)[2] +"\n", "utf-8"))
            elif "/kick" in sendt:
                irc.send(bytes("PRIVMSG ChanServ :kick "+ channel +" "+ sendt.split(" ", 1)[1] + " " + sendt.split(" ",
                                                                                                                   2)
                [2] + "\n", "utf-8"))
            elif "/help" in sendt:
                print("Help:")
                print("@<messageid>|<text> will quote the message at that messageid")
                print("/chan <channel/nick> will switch the chatting channel to to <channel/nick>. \
Ensure that you have joined the channel, if trying to chat on a channel, first")
                print("/join <channel> [password] will join the channel for listening and /chan'ing to to speak")
                print("/quit <message> will quit the server")
                print("/away <message> will set you as away (and change your nickname accordingly)")
                print("/back will un-set you as away (and change your nick back)")
                print("/invite <nick> <channel> will invite <nick> to <channel>")
                print("/kick <nick> will kick <nick> from the current channel")
            elif sendt == "":
                pass
            else:
                irc.send(bytes("PRIVMSG "+ channel +" :" + sendt + "\n", "utf-8"))
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+channel+"] <"+botnick+"> "+sendt
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
        except:
            continue

thread.start_new_thread(send, ())

while True:
    text = str(irc.recv(2040))
    unraw=text.split("\\r\\n")
    for line in unraw:
        try:
            chan = line.split(" :")[0].split(" ")[2]
            nick = line.split(":")[1].split("!")[0]
            text = line.split(":", 2)[2]
            pars = text.lower().split(" ")
        except:
            nick = "Service"
        if server in nick:
            nick = "Service"
        try:
            if nick != "Service":
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] <"+nick+"> "+text
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
                file = open(logdir+"/"+chan+".log", "a")
                file.write("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)]+"\n")
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
            if nickserv:
                irc.send(bytes("PRIVMSG NickServ :IDENTIFY damianos2008\n", "utf-8"))
            if nick != botnick:
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                      +" has joined the channel."
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
        elif line.find("PART :") != -1:
            if nick != botnick:
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                      +" has left the channel: "+line.split(":", 2)[2]+"."
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
        elif line.find("QUIT :") != -1:
            if nick != botnick:
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                      +" has left the server: "+line.split(":", 2)[2]+"."
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
        elif line.find("NICK :") != -1:
            if nick != botnick:
                msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] ["+chan+"] * "+ line.split(":")[1].split("!")[0] \
                    +" has changed their name: "+line.split(":", 2)[2]+"."
                msgs.append(msg)
                print("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
        elif line.find("353") != -1:
            print("*** People currently on channel: "+text)

   #thread.start_new_thread(listen, ())
