import cx_Freeze
import sys

company_name = 'Damian Heaton'
product_name = 'XeIRC IRC Client'
product_version = "0.1.7"

# GUI applications require a different base on Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [cx_Freeze.Executable("client.py",
                                    targetName="xeirc.exe",
                                    shortcutName="XeIRC IRC Client",
                                    shortcutDir="StartMenuFolder",
                                    icon="icon.ico",
                                    base=base),
               cx_Freeze.Executable("client.py",
                                    targetName="xeircDebug.exe",
                                    icon="debicon.ico")]

cx_Freeze.setup(
    name=product_name,
    author=company_name,
    description="A retro-style IRC client. Licensed under GNU GPL v3.",
    version=product_version,
    options={"build_exe": {"packages":["tkinter", "easygui"],
                           "excludes": [],
                           "include_files":["icon.ico", "client.py", "debug.bat"]},
             "bdist_msi": {"upgrade_code" : "{1A72FEAD-E540-480B-B01A-30998AC30F23}",
                           "initial_target_dir" : r'[ProgramFilesFolder]\%s\%s v%s' % (company_name, product_name, product_version),
                           "add_to_path" : True}},
    executables = executables

    )
