import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import os
import sys
import random
import time
import _thread as thread
import easygui

easygui.msgbox("""XeIRC is a community-driven project by Damian Heaton (www.damianheaton.com)
Please see www.xeirc.xyz for help, information, and XeIRC's source code.

XeIRC's source code can also be found with the compiled .exe files for XeIRC:
- If this is a zipped release version, then the source will be a file called
  "client.py" found where you extracted XeIRC to.
- If this is an installed version of XeIRC, navigate to the installation directory;
  the source is a file called "client.py".
- If you're runnning this from source, you know exactly where the source is. :)

XeIRC IRC Client  Copyright (C) 2016  Damian Heaton
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions. Please see the GNU General Public License
version 3 for more information.""")

class ServerDetails(easygui.EgStore):
    def __init__(self, filename):
        self.nickname = "XeIRCUser"
        self.ip = "chat.freenode.com"
        self.port = 6667
        self.channel = "#xeirc"
        self.password = ""
        
        self.filename = filename
        self.restore()

connSettings = ServerDetails("conn.xe")
pre = [
    connSettings.nickname,
    connSettings.ip,
    connSettings.port,
    connSettings.channel,
    connSettings.password
]

details = easygui.multpasswordbox("Please enter IRC Connection Details. \
Settings marked with an asterisk (*) are required.",
                                  "Connect to IRC.", ["Your Nickname (*)", 
                                                      "Server Address (*)", 
                                                      "Server Port (*)", 
                                                      "Channel (*)", 
                                                      "NickServ Password"],
                                  pre)

if details is None:
    sys.exit(0)

connSettings.nickname = details[0]
connSettings.ip = details[1]
connSettings.port = int(details[2])
connSettings.channel = details[3]
connSettings.password = details[4]
connSettings.store()

botnick = connSettings.nickname
server = connSettings.ip
port = connSettings.port
password = connSettings.password
if password == "":
    nickserv = False
else:
    nickserv = True
global primary
primary = [connSettings.channel]
secondary = []

class CommandHelp():
    """
    This class keeps records of the help information of each command and will 
    provide formatted responses as needed by the /help command.
    """
    def __init__(self):
        self.commands = {}
        self.extHelp = {}
    
    def addCommand(self, cmdName, cmdFormat, cmdShortHelp,
                   cmdLongHelp):
        self.commands[cmdName] = [cmdFormat, cmdShortHelp]
        self.extHelp[cmdName] = cmdLongHelp
    
    def listCommands(self):
        entries = []
        for command in self.commands:
            cmdEntry = ("* " + self.commands[command][0]
                        + " :: " + self.commands[command][1])
            entries.append(cmdEntry)
        return entries
    
    def cmdHelp(self, command):
        try:
            helpEntry = ["Help for command \"" + command + "\":",
                         "Format: " + self.commands[command][0],
                         "Description: " + self.extHelp[command]]
            return helpEntry
        except IndexError:
            raise ValueError("The command \"" + command + "\" does not exist.")
    
cmdHelp = CommandHelp()
cmdHelp.addCommand("@", "@<messageid>|<response text>", "This will quote a \
specific message, allowing you to respond clearly.", """@ notation will allow \
you to respond to the message which is identified by messageid with your \
response text. Messageids are shown in brackets ([]) at the beginning of \
logged messages. Some messages (such as system/client messages) are not \
assigned messageids, and so cannot be quoted with @ notation.""")
cmdHelp.addCommand("/showchan", "/showchan", "This will display the \
current channel that you are talking on to you in chat.", """/showchan will \
display the channel that you are currently talking on in chat, similar to \
checking the command list's currently-selected channel (except this one does \
not need a channel selected to show the active channel.)""")
cmdHelp.addCommand("/join", "/join <channel> [password]", "This will join a \
channel with a password if supplied.", """/join will join a channel, using a \
password if you supply one. When you join a channel, you will be able to see \
chat within that channel and talk in the channel. However, /join will not \
automatically set the active channel to the channel that you are joining, and \
so the channel must be manually selected as the active channel in your channel \
list.""")
cmdHelp.addCommand("/quit", "/quit <reason>", "This will quit the server, \
displaying the provided reason along with it.", """/quit will send a QUIT \
request, citing your provided reason, to the connected IRC server. You will \
not be able to chat or see any new messages on the IRC server. Currently, there \
IS NO accompanying /joinserv command to join a server after quitting one.""")
cmdHelp.addCommand("/away", "/away <reason>", "This will set you as away on \
the IRC server, citing the provided reason along with it.", """/away will \
set you as away on the IRC server as a result of the reason provided, alerting \
other users that you will not be able to respond to messages at the moment. It \
will also automatically update your nickname to (your nickname)^away, to show \
that you are away to clients that do not support the AWAY syntax.""")
cmdHelp.addCommand("/back", "/back", "This will undo the effects of the /away \
command.", """/back will mark you as having returned to the IRC server. It \
will also automatically reset your nickname back to its original state, to show \
that you are back to clients that do not support the AWAY syntax.""")
cmdHelp.addCommand("/invite", "/invite <nick> <channel>", "This will invite a user \
to an IRC channel.", """/invite will invite a user to join an IRC channel, additionally \
allowing them to do so if the channel is restricted access, provided that you have \
the rights to do so. It will not necessarily force the user to join the channel.""")
cmdHelp.addCommand("/kick", "/kick <nick>", "This will kick a user from the current \
channel.", """/kick will remove the requested user from the current channel, provided \
that you have the rights to do so on the current channel. Kicks are handled by ChanServ, \
and will not work on a server if ChanServ is not enabled.""")
cmdHelp.addCommand("/names", "/names", "This will display a list of the users currently \
on the active channel.", """/names will display a list of users on the active channel, \
separated by spaces. Ops are represented by an @ next to their name, half-ops shown with &, \
owners shown by ~, and normal users will only show their name.""")
cmdHelp.addCommand("/msg", "/msg <nick> <message>", "This will send a user a private \
message.", """/msg will send the defined user a message, which only they will be able to \
see. They will NOT receive the message if they are offline, due to the volatile nature of \
IRC chat.""")        
        
print("Logging chat to", os.getcwd())

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
irc.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+ botnick +"\n", 
               "utf-8"))
irc.send(bytes("NICK "+ botnick +"\n", "utf-8"))

text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', 
                       "utf-8"))
    elif "433" in line and "Nickname is already in use" in line:
        easygui.msgbox("Nickname already in use. Trying another..."))
        irc.send(bytes("NICK "+ botnick + str(random.randint(1, 100)) + "\n", "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', 
                       "utf-8"))
    
if nickserv:
    irc.send(bytes("PRIVMSG NickServ :IDENTIFY " + password + "\n", 
                   "utf-8"))
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', 
                       "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
print("i")
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', 
                       "utf-8"))
for chan in primary:
    irc.send(bytes("JOIN "+ chan +"\n", "utf-8"))
text = str(irc.recv(2040))
unraw=text.split("\\r\\n")
for line in unraw:
    print(line)
    if line.find("PING :") != -1:
        irc.send(bytes('PONG :' + line.split(" :")[1].upper() + '\r\n', 
                       "utf-8"))
    
root = tk.Tk()
root.title("XeIRC IRC Client")
root.iconbitmap("icon.ico")
frame = tk.Frame(root)
frame.pack(fill='both', expand='yes')
channels = tk.Listbox(frame,
                     height = 2,
                     bg = 'black',
                     fg = "#888478",
                     highlightthickness=0,
                     selectbackground="#4f4f4f",
                     selectforeground="#888478")
channels.pack(fill='x')
channels.insert(tk.END, primary[0])

chatLog = ScrolledText(
    master = frame,
    wrap   = 'word',  # wrap text at full words only
    width  = 25,      # characters
    height = 10,      # text lines
    bg = 'black',        # background color of edit area
    fg = '#0B62ED',
    insertbackground = "#E80860",
    highlightbackground="#888478",
    selectbackground="#E80860",
    selectforeground="#0B62ED"
)
# the padx/pady space will form a frame
chatLog.pack(fill='both', expand="yes")
chat = tk.Text(frame, padx=4, height=1, bg="black", fg="#E80860", insertbackground="#0B62ED",
               selectbackground="#0B62ED", selectforeground="#E80860", highlightthickness=0)
chat.pack(fill='x', side="bottom")
chatLog.config(state="disabled")
def addchat(text):
    chatLog.config(state="normal")
    chatLog.insert("insert", text + "\n")
    chatLog.see(tk.END)
    chatLog.config(state="disabled")
def enterPressed(event):
    #addchat(chat.get("1.0",'end-1c'))
    sendt = chat.get("1.0",'end-2c')
    try:
        pars = sendt.split(" ")
    except:
        pars = [sendt]
    try:
        channel = str(channels.get(channels.curselection()[0]))
    except:
        channel = str(channels.get(0))
    chat.delete("1.0",'end')
    print(sendt)
    if "@" in pars[0]:
        msgid = sendt.split("|")[0].split("@")[1]
        sendt = "\x1d"+msgs[int(msgid)]+"\x1d | " + sendt.split("|")[1]
    if pars[0] == "/chan":
        channel = sendt.split(" ")[1]
    elif pars[0] == "/showchan":
        addchat("Currently chatting on " + channel)
    elif pars[0] == "/join":
        channel = sendt.split(" ")[1]
        irc.send(bytes("JOIN "+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
        channels.insert(tk.END, channel)
    elif pars[0] == "/quit":
        irc.send(bytes("QUIT :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
    elif pars[0] == "/names":
        irc.send(bytes("NAMES :"+ channel +"\n", "utf-8"))
    elif pars[0] == "/away":
        irc.send(bytes("NICK :"+ botnick +"^away\n", "utf-8"))
        irc.send(bytes("AWAY :"+ sendt.split(" ", 1)[1] +"\n", "utf-8"))
    elif pars[0] == "/back":
        irc.send(bytes("AWAY\n", "utf-8"))
        irc.send(bytes("NICK :"+ botnick +"\n", "utf-8"))
    elif pars[0] == "/invite":
        irc.send(bytes("INVITE :"+ sendt.split(" ", 1)[1] + " " + sendt.split(" ", 2)[2] +"\n", "utf-8"))
    elif pars[0] == "/kick":
        irc.send(bytes("PRIVMSG ChanServ :kick "+ channel +" "+ sendt.split(" ", 1)[1] + " " + sendt.split(" ",
                                                                                                           2)
        [2] + "\n", "utf-8"))
    elif pars[0] == "/msg":
        recip = pars[1]
        message = pars = sendt.split(" ", 2)[2]
        irc.send(bytes("PRIVMSG " + recip + " :" + message + "\n", "utf-8"))
        msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] " + botnick + " -> " + recip + ": " + message
        msgs.append(msg)
        addchat("["+str(msgs.index(msg))+"] "+msgs[msgs.index(msg)])
    elif pars[0] == "/help":
        if len(pars) == 1:
            addchat("Help:")
            addchat("Please note that <variables> are required for the command to \
    work, and [variables] are optional. For example, to join #channel (which has \
    no channel password), you would do /join #channel .")
            addchat("To get detailed help on a specific command, do \"/help <command>\"\
    , for example, \"/help @\" will provide help on @ notation, and \"/help /join\" will \
    provide help on the /join command.")
            cmds = cmdHelp.listCommands()
            for cmd in cmds:
                addchat(cmd)
        else:
            try:
                cmd = cmdHelp.cmdHelp(pars[1])
                for line in cmd:
                    addchat(line)
            except ValueError as e:
                addchat("[error] " + e)
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
                chan = "unknown channel"
                nick = "Service"
            if "." in nick:
                nick = "Service"
            if "401" in line:
                addchat("[error] " + text)
            elif "372" in line:
                addchat("[motd] " + text)
            elif "376" in line or "305" in line or "306" in line:
                addchat("[sys] " + text)
            elif "MODE" in line or "366" in line:
                pass
            elif "332" in line:
                addchat("[channel topic] " + text)
            else:
                try:
                    if nick != "Service":
                        if chan != botnick:
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
                        else:
                            msg = "["+time.strftime("%Y.%m.%d %H:%M:%S")+"] " + nick + " -> " + botnick + ": " + text
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