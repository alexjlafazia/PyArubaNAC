from netmiko import ConnectHandler
import getpass, re
from datetime import datetime

start_timeall = datetime.now()

#################################################################
#Adds vlans to L2 Switches
#Including: vlan 40,vlan 50,vlan 66,vlan 70
#Will locate tagged ports on Vlan 999 and apply to all vlans
#Rename vlan 999 to iOT-Trust
#################################################################

def AddL2NACVlan():

    usr = input("Enter Username: ")

    PassWD = getpass.getpass()

    ipsL2 = [line.rstrip("\n") for line in open("iplistL2.txt")]

    for n in ipsL2:

        try:

            ip = n

            start_time = datetime.now()

            net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=PassWD, fast_cli=True, session_log = 'output.txt')

            tagged = net_connect.send_command("show run vlan 999 | inc tagged | ex untagged")

            vlan40 = ["vlan 40","name Staff", tagged, "ip igmp"]
            vlan50 = ["vlan 50","name Student", tagged, "ip igmp"]
            vlan66 = ["vlan 66","name Un-Authenticated", tagged, "ip igmp"]
            vlan70 = ["vlan 70","name iOT-UnTrust", tagged, "ip igmp"]
            vlan999 = ["vlan 999","name iOT-Trust"]

            vlanChange = vlan40 + vlan50 + vlan66 + vlan70 + vlan999

            prompt = net_connect.find_prompt()
            net_connect.send_config_set(vlanChange)
            net_connect.save_config()
            net_connect.disconnect()

            end_time = datetime.now()
            
            #Prints output of switch
            #with open('output.txt', 'r') as output:
            #    print(output.read())

            #Notifies user of completion
            hostname = prompt[:-1]
            print("\n")
            print("#" * 30)
            print (hostname + " " + "-" + " " + "Complete")
            print ("Added New Vlans Successfully")
            print('Duration: {}'.format(end_time - start_time))
            print("#" * 30)

        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)


########################################################################
#Adds vlans to L3 Switches
#Including: vlan 40,vlan 50,vlan 66,vlan 70
#locates tagged ports on Vlan 999 and apply to all vlans
#Locates first 2 octets of sites IP address and creates new IP for vlan
#Rename vlan 999 to iOT-Trust
########################################################################

def AddL3NACVlan():

    usr = input("Enter Username: ")

    PassWD = getpass.getpass()

    ipsL3 = [line.rstrip("\n") for line in open("iplistL3.txt")]

    for n in ipsL3:

        try:

            ip = n

            start_time = datetime.now()
            
            net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=PassWD, fast_cli=True, session_log = 'output.txt')

            tagged = net_connect.send_command("show run vlan 999 | inc tagged | ex untagged")
            ipHelper = net_connect.send_command("show run vlan 999 | inc ip helper")
            ipAddress = net_connect.send_command("show run vlan 999 | inc ip address")

            ipAddr = re.split(r'(\ |\.|/)',ipAddress)

            ipVlan40 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".40.1" + " " + "255.255.252.0"
            ipVlan50 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".52.1" + " " + "255.255.252.0"
            ipVlan66 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".60.1" + " " + "255.255.252.0"
            ipVlan70 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".72.1" + " " + "255.255.252.0"
            ipVlan999 = "ip address" + " " + ipAddr[4] + "." + ipAddr[6] + ".32.1" + " " + "255.255.248.0"

            vlan999 = ["vlan 999","no ip address","name iOT-Trust", ipVlan999,"dhcp-snooping"]
            vlan40 = ["vlan 40","name Staff", tagged, ipVlan40, ipHelper,"dhcp-snooping"]
            vlan50 = ["vlan 50","name Student", tagged, ipVlan50, ipHelper,"dhcp-snooping"]
            vlan66 = ["vlan 66","name Un-Authenticated", tagged, ipVlan66, ipHelper,"dhcp-snooping"]
            vlan70 = ["vlan 70","name iOT-UnTrust", tagged, ipVlan70, ipHelper,"dhcp-snooping"]

            vlanChange = vlan999 + vlan40 + vlan50 + vlan66 + vlan70

            prompt = net_connect.find_prompt()
            net_connect.send_config_set(vlanChange)
            net_connect.save_config()
            net_connect.disconnect()

            end_time = datetime.now()

            #Prints output of switch
            with open('output.txt', 'r') as output:
                print(output.read())

            #Notifies user of completion
            hostname = prompt[:-1]
            print("\n")
            print("#" * 30)
            print (hostname + " " + "-" + " " + "Complete")
            print('Duration: {}'.format(end_time - start_time))
            print("#" * 30)

        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)


########################################################################
#Adds port configurations to L2 Switches
#Including: Radius, Tacacs, aaa settings
#locates untagged ports on Vlan 999 and applies all port configurations
#Adds Key for radius and Tacacs server needs input from user
########################################################################

def AddL2NACPorts():

    usr = input("Enter Username: ")

    PassWD = getpass.getpass()

    radiusKey = input("Enter radius key: ")

    cppmKey = input("Enter CPPM key: ")

    portL2 = [line.rstrip("\n") for line in open("portL2.txt")]


    for n in portL2:

        try:

            ip = n

            start_time = datetime.now()

            net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=PassWD, cppmKey=cppmKey, session_log = 'output.txt')

            untagged = net_connect.send_command("show run vlan 999 | inc untagged")
            untagged = re.sub('[ untagged ]', "", untagged)

            radius = [ 
                "radius-server host 10.1.60.13 key" + " " + key,
                "radius-server host 10.1.60.13 dyn-authorization",
                "radius-server host 10.1.60.13 time-window plus-or-minus-time-window",
                "radius-server host 10.1.60.13 time-window 30",
                "radius-server host 10.1.60.11 key" + " " + key,
                "radius-server host 10.1.60.11 dyn-authorization",
                "radius-server host 10.1.60.11 time-window plus-or-minus-time-window",
                "radius-server host 10.1.60.11 time-window 30",
                "radius-server host 10.1.60.12 key" + " " + key,
                "radius-server host 10.1.60.12 dyn-authorization",
                "radius-server host 10.1.60.12 time-window plus-or-minus-time-window",
                "radius-server host 10.1.60.12 time-window 30",
                "radius-server cppm identity aoss-dur key" + " " + "aoss-dur",
                "aaa authorization user-role enable download",
                "radius-server host 10.1.60.13 clearpass"
            ]

            cert = [
                "crypto ca-download usage clearpass force"
            ]

            tacacs = [
                "timesync ntp",
                "sntp server priority 1 10.1.32.73",
                "ntp enable",
                "tacacs-server host 10.1.60.12",
                "tacacs-server host 10.1.60.11",
                "tacacs-server key" + " " + key,
                "ip client-tracker trusted"
            ]

            aaa = [
                "aaa server-group radius" + ' "' + "CLEARPASS" + '" ' + "host 10.1.60.13",
                "aaa server-group radius" + ' "' + "CLEARPASS" + '" ' "host 10.1.60.11",
                "aaa server-group radius" + ' "' + "CLEARPASS" + '" ' "host 10.1.60.12",
                "aaa accounting update periodic 5",
                "aaa accounting network start-stop radius server-group" + ' "' + "CLEARPASS" + '" ',
                "aaa authorization user-role name" + ' "' + "allowLimited" + '" ',
                    "vlan-id 66",
                    "exit",
                "aaa authorization user-role enable download",
                "aaa authorization user-role initial-role" + ' "' + "allowLimited" + '" ',
                "aaa authentication port-access eap-radius",
                "aaa authentication mac-based chap-radius server-group" + ' "' + "CLEARPASS" + '" ',
            ]

            nacPort = [
                "no port-security" + " " + untagged,
                "aaa port-access authenticator" + " " + untagged,
                "aaa port-access authenticator" + " " + untagged + " " + "tx-period 10",
                "aaa port-access authenticator" + " " + untagged + " " + "supplicant-timeout 10",
                "aaa port-access authenticator" + " " + untagged + " " + "client-limit 8",
                "aaa port-access authenticator active",
                "aaa port-access mac-based" + " " + untagged,
                "aaa port-access mac-based" + " " + untagged + " " + "addr-limit 8",
                "aaa port-access mac-based" + " " + untagged + " " + "addr-moves",
                "aaa port-access mac-based" + " " + untagged + " " + "cached-reauth-period 36000"
            ]

            portChange = radius + cert + tacacs + aaa + nacPort

            prompt = net_connect.find_prompt()
            net_connect.send_config_set(portChange)
            net_connect.send_command("show crypto pki ta-profile")
            net_connect.save_config()
            net_connect.disconnect()

            end_time = datetime.now()

            #Prints output of switch
            with open('output.txt', 'r') as output:
                print(output.read())

            #Notifies user of completion
            hostname = prompt[:-1]
            print("\n")
            print("#" * 30)
            print (hostname + " " + "-" + " " + "Complete")
            print('Duration: {}'.format(end_time - start_time))
            print("#" * 30)

        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)

AddL2NACVlan()

AddL3NACVlan()

AddL2NACPorts()

end_timeall = datetime.now()

#Prints overall time of script
print("\n")
print("#" * 30)
print ("Script" + " " + "Complete")
print('Duration: {}'.format(end_timeall - start_timeall))
print("#" * 30)