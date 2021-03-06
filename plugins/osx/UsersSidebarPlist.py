from riplib.Plugin import Plugin
import codecs
import logging
import os
import riplib.ccl_bplist

__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class UsersSidebarPlist(Plugin):
    """
    Parse information from /Users/<username>/Library/Preferences/com.apple.sidebarlists.plist
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Sidebar Lists Plist"
        self._description = "Parse information from /Users/<username>/Library/Preferences/com.apple.sidebarlists.plist"
        self._data_file = "com.apple.sidebarlists.plist"
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
                    sidebar_plist = os.path.join(users_path, username, "Library", "Preferences", self._data_file)
                    if os.path.isfile(sidebar_plist):
                        self.__parse_bplist(sidebar_plist, username)
                    else:
                        logging.warning("{0} does not exist.".format(sidebar_plist))
                        print("[WARNING] {0} does not exist.".format(sidebar_plist))
        else:
            logging.warning("{0} does not exist.".format(users_path))
            print("[WARNING] {0} does not exist.".format(users_path))

    def __parse_bplist(self, file, username):
        """
        Parse /Users/<username>/Library/Preferences/com.apple.sidebarlists.plist
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_SidebarList.txt"), "a",
                         encoding="utf-8") as of:
            of.write("=" * 10 + " " + self._name + " " + "=" * 10 + "\r\n")
            of.write("Source File: {0}\r\n\r\n".format(file))
            if self.set_os_version in ["high_sierra"]:
                logging.warning("File: com.apple.sidebarlists.plist not in this version.")
                of.write("[INFO] File: com.apple.sidebarlists.plist not in this version.\r\n")
                print("[INFO] File: com.apple.sidebarlists.plist not in this version.")
            elif self._os_version in ["sierra", "el_capitan", "yosemite", "mavericks",
                                    "mountain_lion", "lion", "snow_leopard"]:
                if os.path.isfile(file):
                    bplist = open(file, "rb")
                    plist = riplib.ccl_bplist.load(bplist)
                    try:
                        if "systemitems" in plist:
                            of.write("System Items:\r\n")
                            if "VolumesList" in plist["systemitems"]:
                                volumes = plist["systemitems"]["VolumesList"]
                                for volume in volumes:
                                    if "Name" in volume:
                                        of.write("Name:       {0}\r\n".format(volume["Name"]))
                                    if "EntryType" in volume:
                                        entry_type = volume["EntryType"]
                                        entry_desc = ""
                                        if entry_type == 8:
                                            entry_desc = "Attached Network Drive"
                                        elif entry_type == 16:
                                            entry_desc = "Local"
                                        elif entry_type == 261:
                                            entry_desc = "Internal HDD"
                                        elif entry_type == 515:
                                            entry_desc = "Mounted USB"
                                        elif entry_type == 517:
                                            entry_desc = "Mounted USB HDD"
                                        elif entry_type == 1027:
                                            entry_desc = "Mounted DMG or DVD"
                                        elif entry_type == 1029:
                                            entry_desc = "TimeMachine HDD"
                                        of.write("Entry Type: {0} - {1}\r\n".format(entry_type, entry_desc))
                                    if "Visibility" in volume:
                                        of.write("Visibility: {0}\r\n".format(volume["Visibility"]))
                                    of.write("\r\n")
                    except KeyError:
                        pass
                    bplist.close()
                else:
                    logging.warning("File: {0} does not exist or cannot be found.".format(file))
                    of.write("[WARNING] File: {0} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {0} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("=" * 40 + "\r\n\r\n")
        of.close()
