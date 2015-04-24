__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'

from riplib.Plugin import Plugin
import codecs
import logging
import os
import re


class UsersFaceTimeLog(Plugin):
    """
    Plugin to read /Users/username/Library/Logs/FaceTime/FaceTime.log
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User FaceTime Log"
        self._description = "Read /Users/username/Library/Logs/FaceTime/FaceTime.log"
        self._data_file = "FaceTime.log"
        self._output_file = ""
        self._type = "text"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories and read /Users/username/Library/Logs/FaceTime/FaceTime.log
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    ft_log = os.path.join(users_path, username, "Library", "Logs", "FaceTime", self._data_file)
                    if os.path.isfile(ft_log):
                        self.__parse_facetime_log(ft_log, username)
                    else:
                        logging.warning("{} does not exist.".format(ft_log))
                        print("[WARNING] {} does not exist.".format(ft_log))
        
    def __parse_facetime_log(self, file, username):
        """
        Read the FaceTime.log file
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "yosemite" or self._os_version == "mavericks" or self._os_version == "mountain_lion":
                with codecs.open(file, "r", encoding="utf-8") as ft:
                    for line in ft.readlines():
                        # Received invite push from
                        if "Received invite push from" in line:
                            of.write(line + "\r\n")

                        # VCPropertyNATIP = <
                        if "VCPropertyNATIP = <" in line:
                            line = line.replace("VCPropertyNATIP = <", "").replace(">;", "").replace(" ", "")
                            of.write("VC Property NAT IP: {}\r\n".format(self.__convert_hex_ip(line)))

                        # FZRelayParameter_PeerRelayIP
                        if "FZRelayParameter_PeerRelayIP\" = <" in line:
                            line = line.replace("\"FZRelayParameter_PeerRelayIP\" = <", "").replace(">;", "").replace(" ", "")
                            of.write("FZ Relay Parameter_PeerRelay IP: {}\r\n".format(self.__convert_hex_ip(line)))

                        # FZRelayParameter_SelfRelayIP
                        if "\"FZRelayParameter_SelfRelayIP\" = <" in line:
                            line = line.replace("\"FZRelayParameter_SelfRelayIP\" = <", "").replace(">;", "").replace(" ", "")
                            of.write("FZ Relay Parameter_Self Relay IP: {}\r\n".format(self.__convert_hex_ip(line)))

                        # Found peer ID:
                        if "Found peer ID:" in line:
                            of.write(line + "\r\n")

                        # Choosing callerID
                        if "Choosing callerID" in line:
                            of.write(line + "\r\n")

                        # Found account:
                        if "Found account:" in line:
                            of.write(line + "\r\n")
                        
                        # sendRelayCancelTo:
                        if "sendRelayCancelTo:" in line:
                            of.write(line + "\r\n")

                        # Sending relay cancel to:
                        if "Sending relay cancel to" in line:
                            of.write(line + "\r\n")

                        # Received relay cancel push from
                        if "Received relay cancel push from" in line:
                            of.write(line + "\r\n")

                ft.close()
                
            elif self._os_version == "lion":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()

    @staticmethod
    def __convert_hex_ip(hex_string):
        """
        Converts a list of four bytes to a dotted quad ip address
        """
        ip_address = ""
        hex_list = re.findall('..', hex_string)
        if len(hex_list) == 4:
            for hex_item in hex_list:
                ip_address = ip_address + "{}".format(int(hex_item, 16)) + "."
        else:
            ip_address = "Too many bytes passed to resolve as an IP address."
        return ip_address[:-1]  # trim the trailing .