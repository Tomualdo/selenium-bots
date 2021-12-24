import os

bin_list = [r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            fr"C:\Users\{os.getlogin()}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
            fr"/opt/brave.com/brave/brave-browser",
            # fr"/etc/default/brave-browser",
            # fr"/usr/local/bin/brave-browser"
            ]

def search_binary():
    for b in bin_list:
        if os.path.isfile(b):
            print(f"...binary found at {b}")
            return b
    print (f"...No binary found..running defaults")
    return None
