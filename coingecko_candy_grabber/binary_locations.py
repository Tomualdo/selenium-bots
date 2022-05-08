import os

bin_list = [r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Users\{os.getlogin()}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"]
def search_binary():
    try:
        for b in bin_list:
            if os.path.isfile(b):
                print(f"...binary found at {b}")
                return b
        print (f"...No binary found..running defaults")
        return None
    except Exception as e:
        print(e)
