# -*- coding: utf-8 -*-

"""
    Use this file to put in all the Settings
    - Change according to requirement
"""

# Database Settings
# Default is sqlite
#app_settings["db_type"] = "postgres"
#app_settings["db_host"] = "localhost"
#app_settings["db_port"] = 5432
#app_settings["db_username"] = "web2py"
#app_settings["db_password"] = "web2py"
#app_settings["db_name"] = "newsportal"
#app_settings["db_connection_pool"] = 30
#app_settings["db_migrate"] = True
#app_settings["db_fake_migrate"] = False

# Email settings
#app_settings["mail_server"] = "smtp.gmail.com:587"
#app_settings["mail_tls"] = True
#app_settings["mail_login"] = "email_address:password"
#app_settings["mail_sender_email"] = "'Sender Name' <some_email_address>"

# Language Settings
#app_settings["l10n_readonly"] = True

# Failed Login count
app_settings["failed_login_count"] = 10

# System Settings
app_settings["system_name"] = "Online Newsportal!"

# Password minimum length
app_settings["password_min_length"] = 8

# Auth settings
app_settings["auth_registration_requires_verification"] = False
app_settings["auth_registration_requires_approval"] = False
app_settings["auth_reset_password_requires_verification"] = True
