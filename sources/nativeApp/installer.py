import json
import os
import sys
import winreg

KEYPATH = r'Software\Mozilla\NativeMessagingHosts\Get_Song_Title_To_File'
# Assuming current user overrides local machine.
KEYROOTS = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]

PATHTOFILE  = os.path.dirname(os.path.realpath(sys.argv[0])) 

def createRegistryKeys():
    for root in KEYROOTS:
        try:
            winreg.CreateKey(root, KEYPATH)
            regKey = winreg.OpenKey(root, KEYPATH, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(regKey, None, 0, winreg.REG_SZ, PATHTOFILE + "\Get_Song_Title_To_File.json")
            winreg.CloseKey(regKey);
            print("registry key created")
        except:
            print("Error creating registry key. Try run as administrator")
            return False
    return True

def createJsonFile():
    data = {
        "name": "Get_Song_Title_To_File",
        "description": "Write song title to text file",
        "path": (PATHTOFILE + "\Get_Song_Title_To_File.exe").replace('\\', '/'),
        "type": "stdio",
        "allowed_extensions": [ "1mfSCfd200SongTitleToFile@google.com" ]
    }
    try:
        with open(PATHTOFILE + "\Get_Song_Title_To_File.json", "w+") as outfile:
            outfile.write(json.dumps(data, indent=4))
            outfile.close()
        print("JSON file created")
        return True
    except:
        print("Error creating JSON file")
        return False
    

if createJsonFile() and createRegistryKeys():
    print("\nRESULT: Everything looks good")
else:
    print("\nRESULT: Something gone wrong")
os.system("pause")
