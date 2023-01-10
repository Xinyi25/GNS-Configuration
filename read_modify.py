import json

# Open the JSON configuration file
with open("router_config_test.json", "r") as f:
    # Load the JSON data from the file
    data = json.load(f)

# Make changes to the JSON data
data["router1"]["interface"]["GigabitEthernet1/0"]["ipv6_address"] = "192.168.2.1"

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
                cfg_data += "interface " + intf  
                if cfg_data in line:
                     for intf_key, intf_value in intf_data.items():
                        for j in range(5):
                            if ' ipv6 address' in config_lines[i+j]:
                                #print(config_lines[i+j])
                                config_lines[i+j] = "ipv6 address " + intf_value+ "\n"
                                #print(config_lines[i+j])
                                #print("Interface IP address changed to 192.168.2.1")
                                exit
                            if 'shutdown' in config_lines[i+j]:
                                #print(config_lines[i+j])
                                config_lines[i+j] = "ipv6 address " + intf_value+ "\n"
                                #print(config_lines[i+j])
                                #print("Interface IP address changed to 192.168.2.1")
                                exit

# Write the modified configuration to a new file
with open("router_config_modified.cfg", "w") as f:
    f.writelines(config_lines)
