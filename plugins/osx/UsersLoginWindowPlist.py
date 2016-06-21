from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersLoginWindowPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.loginwindow.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Login Window"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.loginwindow.plist"
        self._data_file = "com.apple.loginwindow.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    plist = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(plist):
                        self.__parse_bplist(plist, username)
                    else:
                        logging.warning("{0} does not exist.".format(plist))
                        print("[WARNING] {0} does not exist.".format(plist))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.loginwindow.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if self._os_version == "el_capitan":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "TALLogoutReason" in pl:
                            of.write("Logout Reason     : {0}\r\n".format(pl["TALLogoutReason"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version in ["yosemite", "mavericks", "mountain_lion"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "TALLogoutReason" in pl:
                            of.write("Logout Reason     : {0}\r\n".format(pl["TALLogoutReason"]))
                        if "TALLogoutSavesState" in pl:
                            of.write("Save State        : {0}\r\n".format(pl["TALLogoutSavesState"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version == "lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "TALLogoutReason" in pl:
                            of.write("Logout Reason        : {0}\r\n".format(pl["TALLogoutReason"]))
                        if "AutoOpenedWindowDictionary" in pl:
                            auto_open = pl["AutoOpenedWindowDictionary"]
                            if "CurrentSpaceID" in auto_open:
                                of.write("Current Space ID     : {0}\r\n".format(auto_open["CurrentSpaceID"]))
                            if "NumberOfSpaces" in auto_open:
                                of.write("Number Of Spaces     : {0}\r\n".format(auto_open["NumberOfSpaces"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
            elif self._os_version == "snow_leopard":
                logging.info("This version of OSX is not supported by this plugin.")
                print("[INFO] This version of OSX is not supported by this plugin.")
                of.write("[INFO] This version of OSX is not supported by this plugin.\r\n")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
