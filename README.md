## GUI version
![Screenshot](https://raw.githubusercontent.com/lilmond/bandwidth-monitor/main/gui/image1.png)

Donwload standalone executable version here: https://github.com/lilmond/bandwidth-monitor/releases/tag/standalone

Source code: https://github.com/lilmond/bandwidth-monitor/tree/main/gui

## Installation and usage
Npcap (required for console version): https://npcap.com/#download
```
pip install -r requirements.txt
python bandwidth_monitor.py
```

## Create your own executable version
If you don't trust the executable version, you are free to compile the source code on your own. Follow the commands below:
```
cd gui
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install PyInstaller
PyInstaller bandwidth_monitor_gui.py --noconsole --onefile --icon NONE --upx-dir ./upx
```
Make sure to copy the gui.ui in the same path with the executable version you built, otherwise, it will fail to run.
