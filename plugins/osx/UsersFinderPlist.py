__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import ccl_bplist


class UsersFinderPlist(Plugin):
    """
    Parse information from /Users/username/Library/Preferences/com.apple.finder.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Mounted Volumes"
        self._description = "Parse information from /Users/username/Library/Preferences/com.apple.finder.plist"
        self._data_file = "com.apple.finder.plist"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "bplist"
    
    def parse(self):
        """
        Iterate over /Users directory and find user sub-directories
        """
        users_path = os.path.join(self._input_dir, "Users")
        # username = None
        if os.path.isdir(users_path):
            user_list = os.listdir(users_path)
            for username in user_list:
                if os.path.isdir(os.path.join(users_path, username)) and not username == "Shared":
                    plist = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(plist):
                        self.__parse_bplist(plist, username)
                    else:
                        logging.warning("{} does not exist.".format(plist))
                        print("[WARNING] {} does not exist.".format(plist))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
            
    def __parse_bplist(self, file, username):
        """
        Parse /Users/username/Library/Preferences/com.apple.finder.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + ".txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            of.write("Source File: {}\r\n\r\n".format(file))
            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks" \
                    or self._os_version == "mountain_lion":
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "FXDesktopVolumePositions" in pl: 
                            for key in pl["FXDesktopVolumePositions"].keys():
                                of.write("Volume     : {}\r\n".format(key))
                        of.write("\r\n")
                        if "FXConnectToLastURL" in pl:
                            of.write("Connect to Last URL: {}\r\n".format(pl["FXConnectToLastURL"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            
            elif self._os_version == "lion" or self._os_version == "snow_leopard":
                #  This needs double checking, none of the DVD, or DMGs mounted are recorded...
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    pl = ccl_bplist.load(bplist)
                    try:
                        if "FXConnectToLastURL" in pl:
                            of.write("Connect to Last URL: {}\r\n".format(pl["FXConnectToLastURL"]))
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()