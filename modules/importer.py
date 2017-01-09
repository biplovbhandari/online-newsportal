# -*- coding: utf-8 -*-

from gluon import current
from gluon.http import HTTP
import csv
import ntpath
import os

class Importer(object):
    """ Importer class to import the prepop data """

    # -------------------------------------------------------------------------
    def __init__(self, filename=None):

        if not filename:
            current.auth.permission.fail()

        self.path = os.path.join(current.app_settings["prepop_files_path"], filename)

        if not os.path.isfile(self.path):
            raise(HTTP(404, "The prepop %s file does not exist!!!" % self.path))

        self.filename = filename
        tablename = self.check_table()

        if not tablename:
            raise(HTTP(404, "Some table(s) are not present for the prepop file!!!"))

        self.tablename = tablename

        import_file = csv.DictReader(open(self.path))
        self.import_file = import_file

    # -------------------------------------------------------------------------
    def check_table(self):

        tablename = self.filename.split(".csv")[0]
        if tablename in current.db.tables:
            return tablename
        return None

    # -------------------------------------------------------------------------
    def import_permission(self):

        auth = current.auth
        create_or_update_group = auth.create_or_update_group

        def parseACL(acl, rules, type=""):
            if not type or type not in ["uacl", "oacl"]:
                raise(HTTP(500, "error with permissions!!!"))

            permissions = acl.split("|")
            if type == "uacl":
                for permission in permissions:
                    if permission == "CREATE":
                        rules["user_create"] = True
                    if permission == "READ":
                        rules["user_read"] = True
                    if permission == "UPDATE":
                        rules["user_update"] = True
                    if permission == "DELETE":
                        rules["user_delete"] = True
            if type == "oacl":
                for permission in permissions:
                    if permission == "CREATE":
                        rules["owner_create"] = True
                    if permission == "READ":
                        rules["owner_read"] = True
                    if permission == "UPDATE":
                        rules["owner_update"] = True
                    if permission == "DELETE":
                        rules["owner_delete"] = True

        roles = {}
        acls = {}
        for row in self.import_file:
            if row != None:
                role = row["role"]
                description = row["description"]
                hidden = row.get("hidden", False)
                rules = {}
    
                controller = row["controller"]
                if controller:
                    rules["controller"] = controller
    
                function = row["function"]
                if function:
                    rules["function"] = function

                tablename = row["table"]
                if tablename:
                    rules["tablename"] = tablename

                uacl = row["uacl"]
                if uacl:
                    parseACL(uacl, rules, type="uacl")
    
                oacl = row["oacl"]
                if oacl:
                    parseACL(oacl, rules, type="oacl")
            if role in roles:
                acls[role].append(rules)
            else:
                roles[role] = [role, description, hidden]
                acls[role] = [rules]

        for role in roles.values():
            create_or_update_group(role[0],
                                   role[1],
                                   role[2],
                                   *acls[role[0]])

# END =========================================================================       