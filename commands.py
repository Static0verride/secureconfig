class Basic:

    class Start:
        en = b"enable \n"
        conf = b"configure terminal \n"
        ex = b"exit \n"
        interface = b"interface "
        ethernet = interface + b"ethernet "


class IPCommand:

    class Dhcp:
        ip = "ip "

        # DHCP-Server foundation
        server = ip + "dhcp-server "

        # DHCP-Client
        client = ip + "dhcp-client "

        # Sub-commands
        server_pool = server + "pool "
        server_enable = (server + "enable \n").encode()
        client_disable = (client + "disable \n").encode()


        # pool sub-sub-commands
        server_pool_network = "network "
        server_pool_tftp = "tftp-server "
        server_pool_exclude = "excluded-address "
        server_pool_deploy = "deploy \n"
        server_pool_bootfile = "bootfile "