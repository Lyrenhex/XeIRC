# XeIRC
### Pronounced "zairc"
Python text-based IRC client with native NickServ support.

XeIRC is an open-source half-text-based half-gui-based IRC client written in Python3.

Making use of Python's multithreading capability, XeIRC has a command-line chat output window, and an easygui "Send message" enterbox.

XeIRC is still in active development and has a lot of capabilities to be added, as all IRC logic is being added in to work with the socket-module backend of XeIRC.

XeIRC also has built-in NickServ password support, however there is currently no support for password-protected servers - these are being worked on.

## How to use
Really, there are two ways to use XeIRC, and it depends on how close to the edge you want to live. ;)
You can either run the latest source build of XeIRC, install a compiled version, run a precompiled standalone release of XeIRC (which will be further behind in development).
The following instructions are provided from a Windows standpoint, and I'm going to guess it should work similarly on Linux. If it doesn't work, please, please, please post an issue!

### Installing a release
1. Navigate to "dist".
2. Run "XeIRC IRC Client-`x.x.x`-win32.msi", where `x.x.x` is the latest version number.
3. Follow the on-screen installation instructions.
4. Launch XeIRC from your Start Menu.
5. You should be met with a command-line window and a separate window asking for IRC connection details; fill it in! (When it asks for a "Password", that's for NickServ; leave it blank if you don't need to authenticate with NickServ.)
6. From there, chat will be displayed in the command-line window, and you can chat in the popup window with a textbox. Try `/help` to see a list of commands currently supported by XeIRC.
7. Have fun! :)

### Running from source
1. First, you need to download Python 3.x (that is, any version of Python 3.2 or above). I can personally vouch for it working on Python 3.4.4. Get it from [the Python website.](http://python.org)
2. Then, you're gonna need to jump into command line and install [Easygui](http://easygui.sourceforge.net/). You can do this through the following:
  1. Open command prompt (Press Windows Key + R, then type cmd.exe and hit enter.)
  2. Type "pip install easygui" (without quotes) and hit enter.
    * IMPORTANT: At this point, you may get an error that "pip" isn't a command; in this case it's not in your path. You can fix this by using the command `C:\PythonX\Scripts\pip.exe install easygui`. (X should be replaced with your Python version's 1st and 2nd numbers without the period; ie, for Python 3.4.x, it would be C:\Python34\Scripts\pip.exe.)
    * Please account for where you installed Python. If you installed it elsewhere (such as in Program Files), then you should replace `C:\PythonX` with wherever Python was installed. Python 3.2 to 3.4 defaultly install to the C: drive, whilst 3.5 will normally install to your Program Files folder.
3. Easygui should install successfully; feel free to ask for help if it doesn't or you don't understand the previous instructions.
4. Run "client.py"; you should be able to run it fine by double-clicking.
5. You should be met with a command-line window and a separate window asking for IRC connection details; fill it in! (When it asks for a "Password", that's for NickServ; leave it blank if you don't need to authenticate with NickServ.)
6. From there, chat will be displayed in the command-line window, and you can chat in the popup window with a textbox. Try `/help` to see a list of commands currently supported by XeIRC.
7. Have fun! :)

### Running from standalone release
1. First, you need to go to the release folder.
2. Extract one of the zip files (probably the latest, would be a good idea) to wherever you want.
3. Run client.exe.
4. You should be met with a command-line window and a separate window asking for IRC connection details; fill it in! (When it asks for a "Password", that's for NickServ; leave it blank if you don't need to authenticate with NickServ.)
5. From there, chat will be displayed in the command-line window, and you can chat in the popup window with a textbox. Try `/help` to see a list of commands currently supported by XeIRC.
6. Have fun! :)