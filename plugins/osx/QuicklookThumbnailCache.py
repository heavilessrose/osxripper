from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3
__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'


class QuicklookThumbnailCache(Plugin):
    """
    Parse information from /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "Quicklook Thumbnail Cache"
        self._description = "Parse information from " \
                            "/private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite"
        self._data_file = "index.sqlite"
        self._output_file = "Quicklook_Thumbnail_Cache.txt"
        self._type = "sqlite"

    def parse(self):
        """
        Read the /private/var/folders/.../com.apple.QuickLook.thumbnailcache/index.sqlite SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, self._output_file), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")

            start_folder = os.path.join(self._input_dir, "private", "var", "folders")
            file_list = []

            # of.write("Source File: {}\r\n\r\n".format(root))
            if self._os_version == "el_capitan" or self._os_version == "yosemite" or self._os_version == "mavericks"\
                or self._os_version == "mountain_lion" or self._os_version == "lion"\
                    or self._os_version == "snow_leopard":
                # search for index.sqlite
                for root, subdirs, files in os.walk(start_folder):
                    if "com.apple.QuickLook.thumbnailcache" in root:
                        if self._data_file in files:
                            file_list.append(os.path.join(root, self._data_file))
                if len(file_list) > 0:
                    for database_file in file_list:
                        if os.path.isfile(database_file):
                            of.write("Source Database: {}\r\n\r\n".format(database_file))
                            conn = None
                            try:
                                conn = sqlite3.connect(database_file)
                                query = "SELECT f.folder,f.file_name,tb.hit_count," \
                                        "datetime(tb.last_hit_date + 978307200, 'unixepoch') FROM files f," \
                                        "thumbnails tb WHERE f.rowid = tb.file_id ORDER BY f.folder, tb.last_hit_date"
                                with conn:
                                    cur = conn.cursor()
                                    cur.execute(query)
                                    rows = cur.fetchall()
                                    if len(rows) > 0:
                                        for row in rows:
                                            if row[0] is None:
                                                of.write("Folder       :\r\n")
                                            else:
                                                of.write("Folder       : {}\r\n".format(row[0]))
                                            if row[1] is None:
                                                of.write("File Name    :\r\n")
                                            else:
                                                of.write("File Name    : {}\r\n".format(row[1]))
                                            if row[2] is None:
                                                of.write("Hit Count    :\r\n")
                                            else:
                                                of.write("Hit Count    : {}\r\n".format(row[2]))
                                            if row[3] is None:
                                                of.write("Last Hit Date:\r\n")
                                            else:
                                                of.write("Last Hit Date: {}\r\n".format(row[3]))
                                            of.write("\r\n")
                                    else:
                                        of.write("No data in dtabase.\r\n")
                                of.write("\r\n")
                            except sqlite3.Error as e:
                                logging.error("{}".format(e.args[0]))
                                print("[ERROR] {}".format(e.args[0]))
                            finally:
                                if conn:
                                    conn.close()
                        of.write("="*50 + "\r\n")
                else:
                    logging.warning("File: index.sqlite does not exist or cannot be found.\r\n")
                    of.write("[WARNING] File: index.sqlite does not exist or cannot be found.\r\n")
                    print("[WARNING] File: index.sqlite does not exist or cannot be found.")
            else:
                logging.warning("Not a known OSX version.")
                print("[WARNING] Not a known OSX version.")
            # of.write("="*40 + "\r\n\r\n")
        of.close()
