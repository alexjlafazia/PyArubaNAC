# PyArubaNAC
Adding vlans for L2 and L3 switches. 

L3 Switch example
'''
vlan 40
   name "Staff"
   tagged A1-A8,B1-B8,C1-C24,D1-D2,D7
   ip helper-address xx.xx.xx.xx
   ip helper-address xx.xx.xx.xx
   ip address xx.xx.xx.xx 255.255.252.0
   dhcp-snooping
   exit
vlan 50
   name "Student"
   tagged A1-A8,B1-B8,C1-C24,D1-D2,D7
   ip helper-address xx.xx.xx.xx
   ip helper-address xx.xx.xx.xx
   ip address xx.xx.xx.xx 255.255.252.0
   dhcp-snooping
   exit
vlan 66
   name "Un-Authenticated"
   tagged A1-A8,B1-B8,C1-C24,D1-D2,D7
   ip helper-address xx.xx.xx.xx
   ip helper-address xx.xx.xx.xx
   ip address xx.xx.xx.xx 255.255.252.0
   dhcp-snooping
   exit
'''
