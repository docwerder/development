import applescript

def mnt_WERDERNAS():

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

def mnt_WERDERNAS2():

    applescript.run('''
        tell application "Finder"
            try
                mount volume "afp://192.168.178.48/WERDERNAS2" as user name "admin" with password "pax123"
            on error
                display dialog "Es ist ein Fehler aufgetreten!" buttons ¬
                {" OK "} default button 1 ¬
                with icon stop
            end try
        end tell
    ''')

def mnt_WERDERNASX():
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

def mnt_WERDERNAS2X():
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