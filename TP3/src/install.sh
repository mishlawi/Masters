#!/usr/bin/env

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt -y install python3-llfuse
    sudo systemctl start mongod.service
    sudo apt -y install python3-pip
    sudo pip3 install pymongo
    sudo pip3 install pyinstaller
    sudo apt -y install python3-pyqt5
    pyinstaller --onefile passthroughfs.py
    pyinstaller --onefile access_control.py
    chmod u+rwx config.ini
    chmod g-rwx config.ini
    chmod o-rwx config.ini
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m pip3 install
    pip3 install pymongo
    pip3 install pyinstaller
    brew install pyqt@5
    pyinstaller --onefile passthroughfs.py
    pyinstaller --onefile access_control.py
    chmod u+rwx config.ini
    chmod g-rwx config.ini
    chmod o-rwx config.ini
fi


