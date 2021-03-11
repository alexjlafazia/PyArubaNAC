from netmiko import ConnectHandler
import getpass, re, logging

def AddL2NACVlan(ip, usr, paswd):

    net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=paswd, fast_cli=True, session_log = 'output.txt')

    tagged = net_connect.send_command("show run vlan 999 | inc tagged | ex untagged")

    vlan40 = ["vlan 40","name Staff", tagged, "ip igmp"]

    vlan50 = ["vlan 50","name Student", tagged, "ip igmp"]

    vlan66 = ["vlan 66","name Un-Authenticated", tagged, "ip igmp"]

    vlan70 = ["vlan 70","name iOT-UnTrust", tagged, "ip igmp"]

    vlan999 = ["vlan 999","name iOT-Trust"]

    net_connect.send_config_set(vlan40)
    net_connect.send_config_set(vlan50)
    net_connect.send_config_set(vlan66)
    net_connect.send_config_set(vlan70)
    net_connect.send_config_set(vlan999)
    net_connect.save_config()
    net_connect.disconnect()
    
    with open('output.txt', 'r') as output:
        print(output.read())

    print (ip + " " + "-" + " " + "Complete")

def AddL3NACVlan(ip, usr, paswd):
    
    net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=paswd, fast_cli=True, session_log = 'output.txt')

    tagged = net_connect.send_command("show run vlan 999 | inc tagged | ex untagged")
    ipHelper = net_connect.send_command("show run vlan 999 | inc ip helper")
    ipAddress = net_connect.send_command("show run vlan 999 | inc ip address")

    ipAddr = re.split(r'(\ |\.|/)',ipAddress)

    ipVlan40 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".40.1" + " " + "255.255.252.0"
    ipVlan50 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".52.1" + " " + "255.255.252.0"
    ipVlan66 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".60.1" + " " + "255.255.252.0"
    ipVlan70 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".70.1" + " " + "255.255.252.0"
    ipVlan999 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".32.1" + " " + "255.255.248.0"

    vlan999 = ["vlan 999","no ip address","name iOT-Trust", ipVlan999]
  
    vlan40 = ["vlan 40","name Staff", tagged, ipVlan40, ipHelper, "dhcp-snooping"]

    vlan50 = ["vlan 50","name Student", tagged, ipVlan50, ipHelper, "dhcp-snooping"]

    vlan66 = ["vlan 66","name Un-Authenticated", tagged, ipVlan66, ipHelper, "dhcp-snooping"]

    vlan70 = ["vlan 70","name iOT-UnTrust", tagged, ipVlan70, ipHelper, "dhcp-snooping"]

    net_connect.send_config_set(vlan999)
    net_connect.send_config_set(vlan40)
    net_connect.send_config_set(vlan50)
    net_connect.send_config_set(vlan66)
    net_connect.send_config_set(vlan70)
    net_connect.save_config()
    net_connect.disconnect()
    
    with open('output.txt', 'r') as output:
        print(output.read())
        
    print (ip + " " + "-" + " " + "Complete")

def AddL2NACPorts(ip, usr, paswd):

    net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=paswd, session_log = output)

ipsL2 = [line.rstrip("\n") for line in open("iplistL2.txt")]
ipsL3 = [line.rstrip("\n") for line in open("iplistL3.txt")]

PassWD = getpass.getpass()

for n in ipsL2:
    AddL2NACVlan(ip=n, usr='nsttech', paswd=PassWD)

for n in ipsL3:
    AddL3NACVlan(ip=n, usr='nsttech', paswd=PassWD)