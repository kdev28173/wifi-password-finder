import  subprocess
import re

output=list()
cmd_output = subprocess.run(["netsh","wlan","show","profiles"],capture_output=True)
cmd_output_decoded = cmd_output.stdout.decode()
profile_name = (re.findall("    All User Profile     : (.*)\r",cmd_output_decoded))

if len(profile_name)!=0:
    for name in profile_name:
        wifi_profile = dict()
        profile_info = subprocess.run(["netsh","wlan","show","profiles",name],capture_output=True)
        profile_info_decoded=profile_info.stdout.decode()
        if re.search("    Security key           : Absent",profile_info_decoded):
            continue
        else:
            wifi_profile['ssid'] = name
            profile_info_clear = subprocess.run(["netsh","wlan","show","profiles",name,"key=clear"],capture_output=True)
            profile_info_clear_decoded = profile_info_clear.stdout.decode()
            password = (re.search("    Key Content            : (.*)\r",profile_info_clear_decoded))
            if password == None:
                wifi_profile['password'] = None
            else:
                wifi_profile['password'] = password[1]
                output.append(wifi_profile)
for i in output:
    print(i)
