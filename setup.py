from cx_Freeze import setup, Executable

execs = [Executable("main.py", icon="mqt.icns")]
include_files = ["MQT_APP.sqlite", "MQT_EX.sqlite"]

setup(
    name = "My Query Tutor",
    version = "1.0",
    description = "A personal tutor to teach you Structured Query Language",
    options =
    {
        "build_exe":
        {
            "include_files":include_files,
            "excludes":['tcl', 'ttk', 'tkinter', 'Tkinter']
        }
    },
    executables=execs, requires=['beautifulsoup4', 'requests', 'PyQt5']
)
