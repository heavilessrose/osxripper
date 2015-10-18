__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class UsersSafariCache(Plugin):
    """
    Parse information from /Users/<username>/Library/Caches/com.apple.safari/Cache.db
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Safari Cache"
        self._description = "Parse information from /Users/<username>/Library/Caches/com.apple.safari/Cache.db"
        self._data_file = "Cache.db"
        self._output_file = ""  # this will have to be defined per user account
        self._type = "sqlite"
    
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
                    sqlite_db = os.path.join(users_path, username, "Library", "Caches", "com.apple.safari", self._data_file)
                    if os.path.isfile(sqlite_db):
                        self.__parse_sqlite_db(sqlite_db, username)
                    else:
                        logging.warning("{} does not exist.".format(sqlite_db))
                        print("[WARNING] {} does not exist.".format(sqlite_db))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the WebpageIcons.db SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Safari_Cache.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks" \
                    or self._os_version == "mountain_lion":
                # query = "SELECT request_key, partition, time_stamp FROM cfurl_cache_response"
                query = "SELECT request_key, time_stamp FROM cfurl_cache_response"
                if os.path.isfile(file):
                    of.write("Source File: {}\r\n\r\n".format(file))
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:    
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("Request Key:\r\n")
                                else:
                                    of.write("Request Key: {}\r\n".format(row[0]))
                                # if row[1] is None:
                                #     of.write("Partition  :\r\n")
                                # else:
                                #     of.write("Partition  : {}\r\n".format(row[1]))
                                if row[1] is None:
                                    of.write("Timestamp  :\r\n")
                                else:
                                    of.write("Timestamp  : {}\r\n".format(row[1]))
                                of.write("\r\n")
                            
                    except sqlite3.Error as e:
                        logging.error("{}".format(e.args[0]))
                        print("[ERROR] {}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            
            elif self._os_version == "lion" or self._os_version == "snow_leopard":
                query = "SELECT request_key, time_stamp FROM cfurl_cache_response"
                if os.path.isfile(file):
                    of.write("Source File: {}\r\n\r\n".format(file))
                    conn = None
                    try:
                        conn = sqlite3.connect(file)
                        with conn:
                            cur = conn.cursor()
                            cur.execute(query)
                            rows = cur.fetchall()
                            for row in rows:
                                if row[0] is None:
                                    of.write("Request Key:\r\n")
                                else:
                                    of.write("Request Key: {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Timestamp  :\r\n")
                                else:
                                    of.write("Timestamp  : {}\r\n".format(row[1]))
                                of.write("\r\n")

                    except sqlite3.Error as e:
                        logging.error("{}".format(e.args[0]))
                        print("[ERROR] {}".format(e.args[0]))
                    finally:
                        if conn:
                            conn.close()
                else:
                    logging.warning("File: {} does not exist or cannot be found.\r\n".format(file))
                    of.write("[WARNING] File: {} does not exist or cannot be found.\r\n".format(file))
                    print("[WARNING] File: {} does not exist or cannot be found.".format(file))
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            of.write("="*40 + "\r\n\r\n")
        of.close()
