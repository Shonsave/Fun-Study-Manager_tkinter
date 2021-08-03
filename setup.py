import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("studymanager.py", base=base, icon="StudyIntervalsIcon.ico")]

cx_Freeze.setup(
    name="Study Manager",
    options={"build_exe": {"packages": ["tkinter", "datetime", "winsound", "PIL"], "include_files": ["StudyIntervalsIcon.ico", "StudyIntervalsLogo.png"]}},
    version="0.01",
    description="A simple application to manage study time and breaks",
    executables=executables
)
