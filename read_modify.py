import json

# Open the JSON configuration file
with open("router_config_test.json", "r") as f:
    # Load the JSON data from the file
    data = json.load(f)

# Make changes to the JSON data
data["router1"]["interface"]["GigabitEthernet1/0"]["ipv6_address"] = "2001:100:100:9::1/64"

##------------------------------------------------------------

import re

# Open the router configuration file
with open("router_config_test_cfg.cfg", "r") as f:
    config_lines = f.readlines()

# Use regular expression to search for the IP address of the interface
for i, line in enumerate(config_lines):
    cfg_data = ""
    for key, value in data["router1"].items():
        if key == "interface":
            for intf, intf_data in value.items():
                ##print(intf) ## 1/0  2/0
                #cfg_data += "interface " + intf  + "\n"
                if intf in line:
                    print(intf)  # 1/0    2/0
                    for j in range(5):   
                        for intf_key, intf_value in intf_data.items():
                            #print(intf_value)
                            if ' ipv6 address' in config_lines[i+j]:
                                config_lines[i+j] = " ipv6 address " + intf_value+ "\n"
                            if 'shutdown' in config_lines[i+j]:
                                config_lines[i+j] = " ipv6 address " + intf_value+ "\n" + " ipv6 enable\n"

# Write the modified configuration to a new file
with open("router_config_modified.cfg", "w") as f:
    f.writelines(config_lines)
