import re

# Open the router configuration file
with open("router_config_test_cfg.cfg", "r") as f:
    config_lines = f.readlines()
#print(config_lines)
# Use regular expression to search for the IP address of the interface
for i, line in enumerate(config_lines):
    if re.search("^interface GigabitEthernet1/0$", line):
        for j in range(5):
            if ' ipv6 address' in config_lines[i+j]:
                print(config_lines[i+j])
                config_lines[i+j] = " ipv6 address 192.168.2.1\n"
                print("Interface IP address changed to 192.168.2.1")
                break

# Write the modified configuration to a new file
with open("router_config_modified.cfg", "w") as f:
    f.writelines(config_lines)
