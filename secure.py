import telnetlib
import sys
import time
from commands import *


class SecureSetup:

    def __init__(self, host, user="", port=23, password=""):
        self.hostname = host
        self.username = user
        self.port = port
        self.password = password
        self.session = None

    def open(self):
        self.session = telnetlib.Telnet(self.hostname, self.port)

    def close(self):
        self.session.close()

    def interact(self):
        self.session.interact()

    def send_command(self, my_list):
        for val in my_list:
            self.session.write(val)

    @staticmethod
    def __creates_list_of_nlines(my_string):
        """ Breaks a long string into separated substring"""
        temp = ""  # sets empty string, will add char respectively
        my_list = list()  # creates list
        for val in range(0, len(my_string)):  # iterates through the length of input
            if my_string[val] == '\n' and temp == "":
                continue
            elif my_string[val] == '\n' or val >= len(my_string):  # add what was found
                my_list.append(temp)
                temp = ""
            else:
                if my_string[val] == ' ' and my_string[val + 1] == '\n':
                    continue
                temp += my_string[val]

        return my_list

    @staticmethod
    def public_nlines(my_string):       # TODO horrible implemenation please fix
        """ Breaks a long string into separated substring"""
        temp = ""  # sets empty string, will add char respectively
        my_list = list()  # creates list
        for val in range(0, len(my_string)):  # iterates through the length of input
            if my_string[val] == '\n' and temp == "":
                continue
            elif my_string[val] == '\n' or val >= len(my_string):  # add what was found
                my_list.append(temp)
                temp = ""
            else:
                if my_string[val] == ' ' and my_string[val + 1] == '\n':
                    continue
                temp += my_string[val]

        return my_list

    def show_version(self):
        self.session.write(b"show version \n")
        return self.session.read_until(b'HW: ', 1).decode('utf-8')

    def show_ip_bindings(self):
        self.session.write(b"show ip dhcp-server binding \n")
        return self.session.read_until(b'None just space', 1).decode('utf-8')

    def default_ssh(self):
        # self.session.read_until(b'(config)#', 1).decode('utf-8')
        cmd = [Basic.Start.en, Basic.Start.conf, b"username admin password pass \n"]
        self.send_command(cmd)
        cmd = [Basic.Start.en, Basic.Start.conf, b"aaa authentication login default local \n"]
        self.send_command(cmd)
        cmd = [Basic.Start.en, Basic.Start.conf, b"crypto key generate \n"]
        self.send_command(cmd)
        time.sleep(10)

    def __show_serial(self):
        self.session.write(b"show version | i Serial \n")
        return self.session.read_until(b'None just space', 1).decode('utf-8')

    def led_on(self):
        cmd = [Basic.Start.en, b"led all on \n"]
        self.send_command(cmd)

    def led_off(self):
        cmd = [Basic.Start.en, b"led all off \n"]
        self.send_command(cmd)

    def obtain_serial(self):
        length = 11                         # length of serial
        output = self.__show_serial()
        token = output.find('#:') + len('#:')
        output = output[token:token+length]
        return output

    def obtain_binding(self):
        find_word = "Hardware address"
        output = self.show_ip_bindings()
        data_dic = dict()
        token = output.find(find_word) + len(find_word) + 1
        nlines = SecureSetup.__creates_list_of_nlines(output[token:len(output)])

        for data in nlines:

            if len(data) <= 1:
                continue
            if 'Telnet' in data or 'Switch' in data:
                continue

            ip, mac, __, __ = data.split()
            data_dic.update({mac: {'ip': ip, 'serial': None, 'type': 'Telnet', 'user': 'NA', 'pwd': 'NA'}})
        return data_dic