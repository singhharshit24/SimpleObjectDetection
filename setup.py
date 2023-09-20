from cx_Freeze import setup, Executable

setup(name="Simple Object Detection",
      version="1.0",
      description="This software detects objects in real time.",
      executables=[Executable("main.py")])