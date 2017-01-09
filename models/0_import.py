# -*- coding: utf-8 -*-

from utility import get_prepop_files
from importer import Importer

auth = current.auth

# create user groups
group_available = auth.check_group()
if not group_available:
    auth.create_system_group()

# Look for prepop files
prepop_files = get_prepop_files()
for filename in prepop_files:
    importer = Importer(filename)
    if filename.split(".csv")[0] == auth.settings.table_permission_name:
        # Import Permission
        importer.import_permission()