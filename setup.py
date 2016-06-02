import cx_Freeze

executables = [cx_Freeze.Executable("client.py",
                                    shortcutName="XeIRC IRC Client",
                                    shortcutDir="StartMenuFolder",
                                    icon="icon.ico")]

cx_Freeze.setup(
    name="XeIRC IRC Client",
    author="Damian Heaton",
    version="0.1.4",
    options={"build_exe": {"packages":["tkinter", "easygui"],
                           "excludes": [],
                           "include_files":["icon.ico"]} },
    executables = executables

    )
