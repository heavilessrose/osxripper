__author__ = 'osxripper'
__version__ = '0.1'
__license__ = 'GPLv3'
from riplib.Plugin import Plugin
import codecs
import logging
import os
import sqlite3


class UsersChromeWebData(Plugin):
    """
    Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Web Data
    """

    def __init__(self):
        """
        Initialise the class.
        """
        super().__init__()
        self._name = "User Chrome Browser Web Data"
        self._description = "Parse information from /Users/<username>/Library/Application Support/Google/Chrome/Default/Web Data"
        self._data_file = "Web Data"
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
                    history_path = os.path.join(users_path, username, "Library", "Application Support", "Google", "Chrome", "Default")
                    if os.path.isdir(history_path):
                        self.__parse_sqlite_db(history_path, username)
                    else:
                        logging.warning("{} does not exist.".format(history_path))
                        print("[WARNING] {} does not exist.".format(history_path))
        else:
            logging.warning("{} does not exist.".format(users_path))
            print("[WARNING] {} does not exist.".format(users_path))
    
    def __parse_sqlite_db(self, file, username):
        """
        Read the Web Data SQLite database
        """
        with codecs.open(os.path.join(self._output_dir, "Users_" + username + "_Chrome_Web_Data.txt"), "a", encoding="utf-8") as of:
            of.write("="*10 + " " + self._name + " " + "="*10 + "\r\n")
            web_data_db = os.path.join(file, "Web Data")
            query = "SELECT name,value,value_lower,datetime(date_created / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch'),datetime(date_last_used / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch'),count FROM autofill"
            if os.path.isfile(web_data_db):
                of.write("Source File: {}\r\n\r\n".format(web_data_db))
                conn = None
                try:
                    conn = sqlite3.connect(web_data_db)
                    with conn:    
                        cur = conn.cursor()
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("Name          :\r\n")
                                else:
                                    of.write("Name          : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Value         :\r\n")
                                else:
                                    of.write("Value         : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Value Lower   :\r\n")
                                else:
                                    of.write("Value Lower   : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Date Created  :\r\n")
                                else:
                                    of.write("Date Created  : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Date Last Used:\r\n")
                                else:
                                    of.write("Date Last Used: {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Count         :\r\n")
                                else:
                                    of.write("Count         : {}\r\n".format(row[5]))
                        else:
                            of.write("No data found in Autofill table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, email FROM autofill_profile_emails"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Emails " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID :\r\n")
                                else:
                                    of.write("GUID : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Email:\r\n")
                                else:
                                    of.write("Email: {}\r\n".format(row[1]))
                        else:
                            of.write("No data found in Autofill Profile Email table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, first_name, middle_name, last_name, full_name FROM autofill_profile_names"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Names " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID       :\r\n")
                                else:
                                    of.write("GUID       : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("First Name :\r\n")
                                else:
                                    of.write("First Name : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Middle Name:\r\n")
                                else:
                                    of.write("Middle Name: {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Last Name  :\r\n")
                                else:
                                    of.write("Last Name  : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Full Name  :\r\n")
                                else:
                                    of.write("Full Name  : {}\r\n".format(row[4]))
                        else:
                            of.write("No data found in Autofill Profile Names table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, number FROM autofill_profile_phones"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Phones " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID        :\r\n")
                                else:
                                    of.write("GUID        : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Phone Number:\r\n")
                                else:
                                    of.write("Phone Number: {}\r\n".format(row[1]))
                        else:
                            of.write("No data found in Autofill Profile Phones table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid,company_name,street_address,dependent_locality,city,state,zipcode,sorting_code,country_code," \
                                "datetime(date_modified / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch'),origin,language_code FROM autofill_profiles"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profiles " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID              :\r\n")
                                else:
                                    of.write("GUID              : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Company Name      :\r\n")
                                else:
                                    of.write("Company Name      : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Street Address    :\r\n")
                                else:
                                    of.write("Street Address    : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Dependent Locality:\r\n")
                                else:
                                    of.write("Dependent Locality: {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("City              :\r\n")
                                else:
                                    of.write("City              : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("State             :\r\n")
                                else:
                                    of.write("State             : {}\r\n".format(row[5]))
                                if row[6] is None:
                                    of.write("Zipcode           :\r\n")
                                else:
                                    of.write("Zipcode           : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("Sorting Code      :\r\n")
                                else:
                                    of.write("Sorting Code      : {}\r\n".format(row[7]))
                                if row[8] is None:
                                    of.write("Country Code      :\r\n")
                                else:
                                    of.write("Country Code      : {}\r\n".format(row[8]))
                                if row[9] is None:
                                    of.write("Date Modified     :\r\n")
                                else:
                                    of.write("Date Modified     : {}\r\n".format(row[9]))
                                if row[10] is None:
                                    of.write("Origin            :\r\n")
                                else:
                                    of.write("Origin            : {}\r\n".format(row[10]))
                                if row[11] is None:
                                    of.write("Language Code     :\r\n")
                                else:
                                    of.write("Language Code     : {}\r\n".format(row[11]))
                        else:
                            of.write("No data found in Autofill Profiles table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid FROM autofill_profiles_trash"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Autofill Profile Trash " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID:\r\n")
                                else:
                                    of.write("GUID: {}\r\n".format(row[0]))
                        else:
                            of.write("No data found in Autofill Profile Trash table.\r\n")
                        of.write("\r\n")

                        query = "SELECT guid, name_on_card, expiration_month, expiration_year, datetime(date_modified / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch'), origin FROM credit_cards"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Credit Cards " + "="*10 + "\r\n")
                        of.write("N.B. Card Number is encrypted. Ommitted by plugin.\r\n\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("GUID            :\r\n")
                                else:
                                    of.write("GUID            : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Name on Card    :\r\n")
                                else:
                                    of.write("Name on Card    : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Expiration Month:\r\n")
                                else:
                                    of.write("Expiration Month: {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("Expiration Year :\r\n")
                                else:
                                    of.write("Expiration Year : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("Date Modified   :\r\n")
                                else:
                                    of.write("Date Modified   : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Origin          :\r\n")
                                else:
                                    of.write("Origin          : {}\r\n".format(row[5]))
                        else:
                            of.write("No data found in Credit Cards table.\r\n")
                        of.write("\r\n")

                        query = "SELECT id,short_name,keyword,favicon_url,url,safe_for_autoreplace,originating_url," \
                                "date_created,usage_count,input_encodings,show_in_default_list,suggest_url,prepopulate_id," \
                                "created_by_policy,instant_url,last_modified,sync_guid,alternate_urls,search_terms_replacement_key," \
                                "image_url,search_url_post_params,suggest_url_post_params,instant_url_post_params,image_url_post_params,new_tab_url FROM keywords"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Keywords " + "="*10 + "\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("ID                          :\r\n")
                                else:
                                    of.write("ID                          : {}\r\n".format(row[0]))
                                if row[1] is None:
                                    of.write("Short Name                  :\r\n")
                                else:
                                    of.write("Short Name                  : {}\r\n".format(row[1]))
                                if row[2] is None:
                                    of.write("Keyword                     :\r\n")
                                else:
                                    of.write("Keyword                     : {}\r\n".format(row[2]))
                                if row[3] is None:
                                    of.write("FavIcon URL                 :\r\n")
                                else:
                                    of.write("FavIcon URL                 : {}\r\n".format(row[3]))
                                if row[4] is None:
                                    of.write("URL                         :\r\n")
                                else:
                                    of.write("URL                         : {}\r\n".format(row[4]))
                                if row[5] is None:
                                    of.write("Safe for Autoreplace        :\r\n")
                                else:
                                    of.write("Safe for Autoreplace        : {}\r\n".format(row[5]))
                                if row[6] is None:
                                    of.write("Originating URL             :\r\n")
                                else:
                                    of.write("Originating URL             : {}\r\n".format(row[6]))
                                if row[7] is None:
                                    of.write("Date Created                :\r\n")
                                else:
                                    of.write("Date Created                : {}\r\n".format(row[7]))
                                if row[8] is None:
                                    of.write("Usage Count                 :\r\n")
                                else:
                                    of.write("Usage Count                 : {}\r\n".format(row[8]))
                                if row[9] is None:
                                    of.write("Input Encodings             :\r\n")
                                else:
                                    of.write("Input Encodings             : {}\r\n".format(row[9]))
                                if row[10] is None:
                                    of.write("Show in Default List        :\r\n")
                                else:
                                    of.write("Show in Default List        : {}\r\n".format(row[10]))
                                if row[11] is None:
                                    of.write("Suggest URL                 :\r\n")
                                else:
                                    of.write("Suggest URL                 : {}\r\n".format(row[11]))
                                if row[12] is None:
                                    of.write("Prepoulate ID               :\r\n")
                                else:
                                    of.write("Prepoulate ID               : {}\r\n".format(row[12]))
                                if row[13] is None:
                                    of.write("Created by Policy           :\r\n")
                                else:
                                    of.write("Created by Policy           : {}\r\n".format(row[13]))
                                if row[14] is None:
                                    of.write("Instant URL                 :\r\n")
                                else:
                                    of.write("Instant URL                 : {}\r\n".format(row[14]))
                                if row[15] is None:
                                    of.write("Last Modified               :\r\n")
                                else:
                                    of.write("Last Modified               : {}\r\n".format(row[15]))
                                if row[16] is None:
                                    of.write("Sync GUID                   :\r\n")
                                else:
                                    of.write("Sync GUID                   : {}\r\n".format(row[16]))
                                if row[17] is None:
                                    of.write("Alternate URLs              :\r\n")
                                else:
                                    of.write("Alternate URLs              : {}\r\n".format(row[17]))
                                if row[18] is None:
                                    of.write("Search Terms Replacement Key:\r\n")
                                else:
                                    of.write("Search Terms Replacement Key: {}\r\n".format(row[18]))
                                if row[19] is None:
                                    of.write("Image URL                   :\r\n")
                                else:
                                    of.write("Image URL                   : {}\r\n".format(row[19]))
                                if row[20] is None:
                                    of.write("Search URL POST Params      :\r\n")
                                else:
                                    of.write("Search URL POST Params      : {}\r\n".format(row[20]))
                                if row[21] is None:
                                    of.write("Suggest URL POST Params     :\r\n")
                                else:
                                    of.write("Suggest URL POST Params     : {}\r\n".format(row[21]))
                                if row[22] is None:
                                    of.write("Instant URL POST Params     :\r\n")
                                else:
                                    of.write("Instant URL POST Params     : {}\r\n".format(row[22]))
                                if row[23] is None:
                                    of.write("Image URL POST Params       :\r\n")
                                else:
                                    of.write("Image URL POST Params       : {}\r\n".format(row[23]))
                                if row[24] is None:
                                    of.write("New Tab URL                 :\r\n")
                                else:
                                    of.write("New Tab URL                 : {}\r\n".format(row[24]))
                                of.write("\r\n")
                        else:
                            of.write("No data found in Keywords table.\r\n")
                        of.write("\r\n")

                        query = "SELECT service FROM token_service"
                        cur.execute(query)
                        rows = cur.fetchall()
                        of.write("="*10 + " Token Service " + "="*10 + "\r\n")
                        of.write("N.B. Service tokens are encrypted. Not retrieved by this plugin\r\n\r\n")
                        if len(rows) != 0:
                            for row in rows:
                                if row[0] is None:
                                    of.write("Service:\r\n")
                                else:
                                    of.write("Service: {}\r\n".format(row[0]))
                        else:
                            of.write("No data found in Token Service table.\r\n")
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
            of.write("="*40 + "\r\n\r\n")
        of.close()