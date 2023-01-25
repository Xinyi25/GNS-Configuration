import json
import os


# Open the JSON configuration file
with open("router_config_test.json", "r") as f:
    # Load the JSON data from the file
    print("iii")
    data = json.load(f)


    

# Make changes to the JSON data
#data["router1"]["interface"]["GigabitEthernet1/0"]["ipv6_address"] = "2001:100:100:9::1/64"
for Router,Router_info in data["AS100"]["Router"].items():
    #print(Router_info)
    for router_key, router_value in Router_info.items():
        #print(router_key)
        #if router_key == "hostmane":
           # router_id = router_value
        router_id = Router_info["hostname"]
        link = Router_info["link"]
        #print(link)
        ip = []
        border = Router_info["border"]
        ip.append("2001:100:100:100::"+router_id +"/128")
        for i in range(len(link)):
            voisin = link[i]
            if router_id < voisin:
                address = "2001:100:100:"+ router_id + voisin +"::"+router_id +"/64"
            else:
                address = "2001:100:100:"+ voisin + router_id +"::"+router_id +"/64"
            #print(address)
            ip.append(address)
            #interface[i] = {_,address}
            #print(len(Router_info["interface"].items())
        for j in range(len(border)):
            peer_voisin = border[j]
            #print(peer_voisin)
            if router_id < peer_voisin:
                address_peer = "2001:100:1:"+router_id+peer_voisin+"::"+router_id +"/64"
            else:
                address_peer = "2001:100:1:"+peer_voisin+router_id+"::"+router_id +"/64"
            ip.append(address_peer)
            #print(ip)
        k = 0
        #print(ip)
        for interfaceX , ipv6_address in Router_info["interface"].items():
            #interfaceX[ipv6_address] = ip[i]
            #print(len(ip))
            #print( router_id+"   ->   "+interfaceX + "   ->   " + ip[k])
            Router_info["interface"][interfaceX]["ipv6_address"]= ip[k]
            k +=1

for Router,Router_info in data["AS200"]["Router"].items():
    #print(Router_info)
    for router_key, router_value in Router_info.items():
        #print(router_key)
        #if router_key == "hostmane":
           # router_id = router_value
        router_id = Router_info["hostname"]
        link = Router_info["link"]
        #print(link)
        ip = []
        border = Router_info["border"]
        ip.append("2001:200:200:200::"+router_id +"/128")
        for i in range(len(link)):
            voisin = link[i]
            if router_id < voisin:
                address = "2001:200:200:"+ router_id + voisin +"::"+router_id +"/64"
            else:
                address = "2001:200:200:"+ voisin + router_id +"::"+router_id +"/64"
            #print(address)
            ip.append(address)
            #interface[i] = {_,address}
            #print(len(Router_info["interface"].items())
        for j in range(len(border)):
            peer_voisin = border[j]
            #print(peer_voisin)
            if router_id < peer_voisin:
                address_peer = "2001:100:1:"+router_id+peer_voisin+"::"+router_id +"/64"
            else:
                address_peer = "2001:100:1:"+peer_voisin+router_id+"::"+router_id +"/64"
            ip.append(address_peer)
            #print(ip)
        k = 0
        for interfaceX , ipv6_address in Router_info["interface"].items():
            #interfaceX[ipv6_address] = ip[i]
            #print(len(ip))
            #print( router_id+"   ->   "+interfaceX + "   ->   " + ip[k])
            Router_info["interface"][interfaceX]["ipv6_address"]= ip[k]
            k +=1
        

#print(data["AS100"]["Router"]["router1"]["interface"]["GigabitEthernet2/0"]["ipv6_address"])



#------------------------------------------------------------

import re

#-----------------------------AS = { AS100, AS200 }----------------------------------------------------
for AS, AS_info in data.items():
    print(AS)
    #---------------AS_Router_Protocole = { AS_nom, Protocole, Router }---------------------------------
    for AS_Router_Protocole, AS_Router_Protocole_info in AS_info.items():
        #print(AS_Router_Protocole)
        # Variable "protocole"
        if AS_Router_Protocole == "Protocole":
            proto =  AS_Router_Protocole_info
            #print(proto)
        #------------------------Section Router-------------------------------------------------------
        if AS_Router_Protocole == "Router":
            #print(AS_Router)
            #----------------------router = { router1, router2, router3,.....}-------------------------
            for router, router_info in AS_Router_Protocole_info.items():
                    # Open the router configuration file
                with open("router_config_test_cfg.cfg", "r") as f:
                    print("Open")
                    config_lines = f.readlines()
                    for i, line in enumerate(config_lines):
                        cfg_data = ""
                        #------------------key = { hostname, interface }------------------------------
                        for key, value in router_info.items():
                            #print(key)
                            border = router_info["border"]
                            if key == "hostname":
                                router_id = value
                                if key in line:
                                    #print(value) ## routerX 
                                    config_lines[i] = "hostname R"+ value + "\n"
                            if key == "interface":
                                #print(key)
                                #------------intf = { GigabitEthernet1/0, ...2/0, ...3/0,... }----------------
                                for intf, intf_data in value.items():
                                    #print(intf) ## 1/0  2/0
                                    #cfg_data += "interface " + intf  + "\n"
                                    if intf in line:
                                        #print(intf)  # 1/0    2/0
                                        #-------------intf_key = { ipv6_address, bord }-----------------------------
                                        for intf_key, intf_value in intf_data.items():
                                            config_lines[i+2] = ""
                                            config_lines[i+4] = " ipv6 address " + intf_data["ipv6_address"]+ "\n ipv6 enable\n"

                                            if intf_data["bord"] == False:
                                                if (proto == "RIP"):
                                                    config_lines[i+4] += " ipv6 rip ripng enable\n!\n"
                                                if (proto == "OSPF"):
                                                    config_lines[i+4] += " ipv6 ospf "+router_id+" area 0\n!\n"
                        #--------------Add Protocle informations--------------------------
                        #print(router_id)
                        if "no ip http secure-server" in line: 
                            if proto == "RIP":
                                config_lines[i+2] = "ipv6 router rip ripng\n redistribute connected\n!\n"
                            if proto == "OSPF":
                                #print(proto)
                                config_lines[i+2] = "ipv6 router ospf "+router_id+" \n router-id "+router_id+"."+router_id+"."+router_id+"."+router_id+"\n!\n"
                                #print(router_id)                       
                    
                # Write the modified configuration to a new file
                with open("i"+router_id+"_startup-config.cfg", "w") as f:
                    f.writelines(config_lines)   
 
list_AS = []
for AS,AS_value in data.items():
    list_AS.append(AS_value["AS_nom"])
print(list_AS)
#BGP table ASX
for asx in range(len(list_AS)):
    ASX = list_AS[asx]

    for Router,Router_info in data["AS"+ASX]["Router"].items():
        router_id = Router_info["hostname"]
        border = Router_info["border"]
        ip_neighbor = []
        ip_activate = []
        peer_id = []
        ip_network = []
        #print("!!!!!"+Router)
        for RouterX,RouterX_info in data["AS"+ASX]["Router"].items():
            #print(Router_info)
            if router_id != RouterX_info["hostname"]:
                for intf_key, intf_value in RouterX_info["interface"].items():
                    if intf_key == "Loopback0":
                        ip_neighbor.append("neighbor "+intf_value["ipv6_address"].split("/")[0]+" remote-as "+ASX+" \n neighbor "+intf_value["ipv6_address"].split("/")[0]+" update-source Loopback0")
                        ip_activate.append("neighbor "+intf_value["ipv6_address"].split("/")[0]+" activate")
                    else:
                        if " network "+intf_value["ipv6_address"].split("::")[0] + "::/64" not in ip_network and intf_value["bord"] == False:
                            ip_network.append(" network "+intf_value["ipv6_address"].split("::")[0] + "::/64")

            else:
                for intf_key, intf_value in RouterX_info["interface"].items():
                    if intf_value["bord"] == True:
                        peer_id.append(intf_value["ipv6_address"])

        if len(border) != 0:
            for j in range(len(border)):
                peer_voisin = border[j]
                for x in range(len(list_AS)):
                    asx = list_AS[x]
                    if asx != ASX:
                        for intfG, intfG_info in data["AS"+asx]["Router"]["router"+peer_voisin]["interface"].items():
                            if intfG_info["bord"] == True:
                                ip_neighbor.append("neighbor "+intfG_info["ipv6_address"].split("/")[0]+" remote-as "+asx)
                                ip_activate.append("neighbor "+intfG_info["ipv6_address"].split("/")[0]+" activate")
        #print("\n{}".format(ip_neighbor))
        with open("i"+router_id+"_startup-config.cfg", "r") as f1:
            print("Open")
            config_lines = f1.readlines()
            for i, line in enumerate(config_lines):
                if "ip forward-protocol nd" in line:
                    config_lines[i-1] = "!\nrouter bgp "+ASX+" \n" + " bgp router-id " +router_id+"."+router_id+"."+router_id+"."+router_id+"\n"
                    config_lines[i-1] = config_lines[i-1] + " bgp log-neighbor-changes\n"+" no bgp default ipv4-unicast\n"
                    for p in range(len(ip_neighbor)):
                        config_lines[i-1] += " " + ip_neighbor[p] +"\n"
                    #config_lines[i-1] += "!\n" +" address-family ipv4\n exit-address-family\n!\n address-family ipv6\n"
                    config_lines[i-1] += "!\n" +" address-family ipv6\n"
                    if len(border) != 0:
                        for n in range(len(peer_id)):
                            prefix = peer_id[n][0:15]
                            print("prefix",prefix)
                            config_lines[i-1]+="  network "+prefix + "/64\n"
                        for m in range(len(ip_network)):
                            config_lines[i-1] += " " + ip_network[m] +"\n"
                    for p in range(len(ip_activate)):
                        config_lines[i-1] += "  " + ip_activate[p] +"\n"
                    config_lines[i-1] += " exit-address-family\n!\n"
            

        with open("i"+router_id+"_startup-config.cfg", "w") as f1:
            f1.writelines(config_lines)

# #router1
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i1_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/0a8fb1a1-bb92-4ad7-a885-81c61be16498/configs/i1_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router2
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i2_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/88c418ce-4233-4cea-89b3-207284a41a61/configs/i2_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router3
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i3_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/eb54c651-c92d-4bbe-8c27-6b81ac23d67e/configs/i3_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router4
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i4_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/04cbd9a4-0ea3-41c6-b364-0915eb2d220c/configs/i4_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router5
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i5_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/632e09fb-7ea2-4af8-9f14-8cd653153d67/configs/i5_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router6
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i6_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/6a8195c2-55b3-4b10-8f7d-50d7b4c61a4b/configs/i6_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router7
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i7_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/6587b49d-b020-4a49-af3d-3e5bf5a4e625/configs/i7_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router8
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i8_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/06f63c8f-9d23-4c1c-a255-7e715b4aba8b/configs/i8_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router9
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i9_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/99b287ee-733a-40cb-941d-bc01100365ab/configs/i9_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router10
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i10_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/5f2d9c6b-c6ff-4e2b-ad10-f46dc65a01c2/configs/i10_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router11
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i11_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/364d7188-bdce-4fb6-a9b0-9e9ea1860b48/configs/i11_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router12
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i12_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/a902804f-7ef0-4a5e-8b46-80c9fa346359/configs/i12_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router13
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i13_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/de28204b-677f-436c-b95a-c63b62c12e41/configs/i13_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

# #router14
# src_file = '/mnt/c/Users/Lenovo/Desktop/3A/GNS3/GNS-Configuration/i14_startup-config.cfg'
# dst_file = '/mnt/c/Users/Lenovo/GNS3/projects/GNS_config_auto/project-files/dynamips/a9b3e61b-8852-4fca-88db-5d983399d591/configs/i14_startup-config.cfg'
# # use the os.replace() function to copy the file and replace if already exist
# os.replace(src_file, dst_file)

