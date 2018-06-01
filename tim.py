from secure import *
from napalm_ruckus_fastiron import *

# e.g data_file = 'C:/User/compname/Desktop/readme.txt'
init_ssh = None
data_file = 'C:/Users/jmendez/Documents/Napalm/table.txt'
sec_config = 'C:/Users/jmendez/Documents/Napalm/serial_conf.txt'

secure_connection = ['Local/Administrator', '1']

mac_list = list()                               # used to identify bind devices
file = ''

""" Opens file and grabs mac and appends to mac_list"""
try:
    temp_file = open(data_file, 'r')                # Opens file as read only
    for sentence in temp_file:                      # Grabs pre-existing data
        temp_mac, __, __, __, __, __ = sentence.split()     # segregates data
        mac_list.append(temp_mac)                   # adds mac data to list
    temp_file.close()                               # close file
except IOError:                                     # file is empty will continue
    pass

""" Connect to DHCP Server and obtain bindings"""
DHCP_Server = SecureSetup('10.176.217.148')        # Connects to ICX DHCP Server
DHCP_Server.open()                              # Opens connection
bindings = DHCP_Server.obtain_binding()         # Parses bindings returns dictionary

""" Save bindings to a file"""
file = open(data_file, 'a')                     # Opens saving file
for mac_key in bindings:                        # grabs mac
    if mac_key not in mac_list:                 # checks if device not in binding
        mac_list.append(mac_key)                # new device added to binding
        ip = bindings.get(mac_key).get('ip')    # ip add for telnet
        ser = bindings.get(mac_key).get('serial')   # serial for later conversion
        con = bindings.get(mac_key).get('type')
        usr = bindings.get(mac_key).get('user')
        pas = bindings.get(mac_key).get('pwd')
        temp_string = mac_key + " " + ip + " " + str(ser) + " " + con + " " + usr + " " + pas + '\n'
        file.write(temp_string)                 # saved to file as single string
file.close()                                    # closed file
DHCP_Server.close()                             # DHCP server connection closed

"""Connect to devices using IP bindings obtained"""
current_file = open(data_file, 'r')             # Reads data populated in text
book_keeping = list()                           # Dynamic memory for updating con

for data in current_file.readlines():           # Reads line by line of text
    mac, ip, serial, type_con, user, pas = data.split()
    telnet_switch = SecureSetup(ip)                #
    telnet_switch.open()                        #

    """Grab serial number of switch"""
    if serial == "None":
        serial = telnet_switch.obtain_serial()

    """Push default security configuration"""
    if init_ssh is None and type_con == "Telnet":   # Default ssh parameters accepted
        print(ip)
        telnet_switch.default_ssh()
        telnet_switch.led_on()
        book_keeping.append([mac, ip, serial, 'SSH', 'admin', 'pass'])

    book_keeping.append([mac, ip, serial, 'SSH', 'admin', 'pass'])      # TODO add file change in param

    """Turn on LED of Switch to symbolize Process has started"""
    telnet_switch.close()                       #
current_file.close()

"""Updating all parameters in document"""
update_file = open(data_file, 'w')              # OVERWRITE
for switch in book_keeping:
    t_str = switch[0] + " " + switch[1] + " " + switch[2] + " " + switch[3] + " " + switch[4] + \
            " " + switch[5] + '\n'
    update_file.write(t_str)
update_file.close()

"""Use napalm to secure connect to switch"""

temp_file = open(sec_config, 'r')
my_file = temp_file.read()
nlines = SecureSetup.public_nlines(my_file)

for switch_info in book_keeping:
    ip = switch_info[1]
    cereal = switch_info[2]
    connect_type = switch_info[3]
    user = switch_info[4]
    pwd = switch_info[5]
    print(ip, " ", user, " ", pwd)

    device = FastIronDriver(ip, user, pwd)
    device.open()

    for config in nlines:
        serial, scp_ip, file_name = config.split()
        if cereal == serial:
            device.enable()
            cmd = ['copy scp running-config ' + scp_ip + " " + file_name] + secure_connection
            print(cmd)
            device.send_config(cmd)
    device.close()

sys.exit(10)

for switch_info in book_keeping:
    ip = switch_info[1]

    telnet_switch = SecureSetup(ip)
    telnet_switch.open()
    telnet_switch.led_off()
    telnet_switch.close()

