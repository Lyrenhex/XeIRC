import cx_Freeze

executables = [cx_Freeze.Executable("client.py")]

cx_Freeze.setup(
    name="XeIRC IRC Client",
    author="Damian Heaton",
    options={"build_exe": {"packages":["tkinter", "easygui"],
                           "excludes": [],
                           "include_files":[]} },
    executables = executables

    )
