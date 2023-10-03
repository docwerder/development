import applescript
import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QPushButton, QLabel, QDialog ,QDialogButtonBox, QVBoxLayout, QMessageBox

class mountToWerderNas():
    # print("Import of class mountToWerderNas successfully! ")
    def __init__(self):
        pass
        # print("Initialization of class mountToWerderNas successfully! ")
    
    def execute_applescript_werdernas():
        # print("Apple Script WERDERNAS before successfully executed!")
        applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS" as user name "admin" with password "pax123"
            
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬ 
                with icon stop
            end try
        end tell
    ''')
        # print("Apple Script WERDERNAS after successfully executed!")


########################
class mountToWerderNas2():
    # print("Import of class mountToWerderNas2 successfully! ")
    def __init__(self):
        pass
        # print("Initialization of class mountToWerderNas2 successfully! ")
    
    def execute_applescript_werdernas2():
        # print("Apple Script WERDERNAS2 before successfully executed!")
        applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS2" as user name "admin" with password "pax123"
                display dialog "Mount to WERDERNAS2 successfull!"
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end 
            try
        end tell
    ''')
        # print("Apple Script WERDERNAS2 after successfully executed!")


#################
class mountToWerderNasx():
    # print("Import of class mountToWerderNasx successfully! ")
    def __init__(self):
        pass
        # print("Initialization of class mountToWerderNasx successfully! ")
    
    def execute_applescript_werdernasx():
        # print("Apple Script WERDERNASX before successfully executed!")
        applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNASX" as user name "admin" with password "pax123"
            
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')
        # print("Apple Script WERDERNASX after successfully executed!")


#############

class mountToWerderNas2x():
    # print("Import of class mountToWerderNas2x successfully! ")
    def __init__(self):
        pass
        # print("Initialization of class mountToWerderNas2x successfully! ")
    
    def execute_applescript_werdernas2x():
        # print("Apple Script WERDERNAS2X before successfully executed!")
        applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS2X" as user name "admin" with password "pax123"
            
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')
        # print("Apple Script WERDERNAS2X after successfully executed!")


######### Unmount-classes

class unMountWerderNas():
    def execute_applescript_unmount_werdernas():
        # print("Apple Script UNMOUNT WERDERNAS before!")
        applescript.run('''
        set volumes_ to {"WERDERNAS"}
        tell application "Finder"
            repeat with vol_ in volumes_
                eject disk vol_
            end repeat
        end tell
        ''')
        print("UNMOUNT WERDERNAS!")


###################
class unMountWerderNas2():
    def execute_applescript_unmount_werdernas2():
        # print("Apple Script UNMOUNT WERDERNAS2 before!")
        applescript.run('''
        set volumes_ to {"WERDERNAS2"}
        tell application "Finder"
            repeat with vol_ in volumes_
                eject disk vol_
            end repeat
        end tell
        ''')
        print("UNMOUNT WERDERNAS2!")


###################
class unMountWerderNasx():
    def execute_applescript_unmount_werdernasx():
        # print("Apple Script UNMOUNT WERDERNASX before!")
        applescript.run('''
        set volumes_ to {"WERDERNASX"}
        tell application "Finder"
            repeat with vol_ in volumes_
                eject disk vol_
            end repeat
        end tell
        ''')
        print("UNMOUNT WERDERNASX!")



#############
class unMountWerderNas2x():
    def execute_applescript_unmount_werdernas2x():
        # print("Apple Script UNMOUNT WERDERNAS2X before!")
        applescript.run('''
        set volumes_ to {"WERDERNAS2X"}
        tell application "Finder"
            repeat with vol_ in volumes_
                eject disk vol_
            end repeat
        end tell
        ''')
        print("UNMOUNT WERDERNAS2X!")