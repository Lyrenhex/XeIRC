import cx_Freeze

executables = [cx_Freeze.Executable("client.py")]

cx_Freeze.setup(
    name="XeIRC IRC Client",
    author="Adonis Megalos",
    version="0.0.0.1",
    options={"build_exe": {"packages":[],
                           "excludes": [],
                           "include_files":[]} },
    executables = executables

    )
