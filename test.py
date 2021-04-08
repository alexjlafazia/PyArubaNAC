from netmiko import ConnectHandler
import getpass, re

#################################################################
#Adds vlans to L2 Switches
#Including: vlan 40,vlan 50,vlan 66,vlan 70
#Will locate tagged ports on Vlan 999 and apply to all vlans
#Rename vlan 999 to iOT-Trust
#################################################################

def AddL2NACPorts(ip, usr, paswd, key):

    net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=paswd, session_log = 'output.txt')

    untagged = net_connect.send_command("show run vlan 999 | inc untagged")
    untagged = re.sub('[ untagged ]', "", untagged)

    radius = [ 
        "radius-server host 10.1.60.13 key " + key,
        "radius-server host 10.1.60.13 dyn-authorization",
        "radius-server host 10.1.60.13 time-window plus-or-minus-time-window",
        "radius-server host 10.1.60.13 time-window 30",
        "radius-server host 10.1.60.11 key " + key,
        "radius-server host 10.1.60.11 dyn-authorization",
        "radius-server host 10.1.60.11 time-window plus-or-minus-time-window",
        "radius-server host 10.1.60.11 time-window 30",
        "radius-server host 10.1.60.12 key " + key,
        "radius-server host 10.1.60.12 dyn-authorization",
        "radius-server host 10.1.60.12 time-window plus-or-minus-time-window",
        "radius-server host 10.1.60.12 time-window 30",
        "radius-server cppm identity aoss-dur key " + key,
        "aaa authorization user-role enable download",
        "radius-server host 10.1.60.13 clearpass"
    ]

    print (radius)

portL2 = [line.rstrip("\n") for line in open("portL2.txt")]

PassWD = getpass.getpass()

radiusKey = input("Enter radius key: ")

for n in portL2:
    AddL2NACPorts(ip=n, usr='nsttech', paswd=PassWD, key=radiusKey)