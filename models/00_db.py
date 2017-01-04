# -*- coding: utf-8 -*-

"""
    Configure the Database
"""

get_app_settings = app_settings.get
migrate = get_app_settings("db_migrate", True)
fake_migrate = get_app_settings("db_fake_migrate", False)

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if get_app_settings("l10n_readonly", True):
    # Make the Language files read-only for improved performance
    T.is_writable = False

########################
# Database Configuration
########################

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db_type = get_app_settings("db_type", "sqlite").lower()
    pool_size = get_app_settings("pool_size", 30)
    
    if db_type == "sqlite":
        db_string = "sqlite://storage.db"
    elif db_type == "mysql":
        db_string = "mysql://%s:%s@%s:%s/%s" % \
                    (get_app_settings("db_username", "web2py"),
                     get_app_settings("db_password", "web2py"),
                     get_app_settings("db_host", "localhost"),
                     get_app_settings("db_port") or "3306",
                     get_app_settings("db_name", "newsportal"))
    elif (db_type == "postgres"):
        db_string = "postgres://%s:%s@%s:%s/%s" % \
                    (get_app_settings("db_username", "web2py"),
                     get_app_settings("db_password", "web2py"),
                     get_app_settings("db_host", "localhost"),
                     get_app_settings("db_port") or "5432",
                     get_app_settings("db_name", "newsportal"))
    else:
        from gluon import HTTP
        raise HTTP(501, body="Database type '%s' not recognised - please correct file models/000_config.py." % db_type)
    
    if db_string.find("sqlite") != -1:
        if migrate:
            check_reserved = ("mysql", "postgres")
        else:
            check_reserved = []
        db = DAL(db_string,
                 check_reserved=check_reserved,
                 migrate_enabled = migrate,
                 fake_migrate_all = fake_migrate,
                 lazy_tables = not migrate)
        # on SQLite 3.6.19+ this enables foreign key support (included in Python 2.7+)
        # db.executesql("PRAGMA foreign_keys=ON")
    else:
        try:
            if db_string.find("mysql") != -1:
                # Use MySQLdb where available (pymysql has given broken pipes)
                # - done automatically now, no need to add this manually
                #try:
                #    import MySQLdb
                #    from gluon.dal import MySQLAdapter
                #    MySQLAdapter.driver = MySQLdb
                #except ImportError:
                #    # Fallback to pymysql
                #    pass
                if migrate:
                    check_reserved = ["postgres"]
                else:
                    check_reserved = []
                db = DAL(db_string,
                         check_reserved = check_reserved,
                         pool_size = pool_size,
                         migrate_enabled = migrate,
                         fake_migrate_all = fake_migrate,
                         lazy_tables = not migrate)
            else:
                # PostgreSQL
                if migrate:
                    check_reserved = ["mysql"]
                else:
                    check_reserved = []
                db = DAL(db_string,
                         check_reserved = check_reserved,
                         pool_size = pool_size,
                         migrate_enabled = migrate,
                         fake_migrate_all = fake_migrate,
                         lazy_tables = not migrate)
        except:
            db_type = db_string.split(":", 1)[0]
            db_location = db_string.split("@", 1)[1]
            raise(HTTP(503, "Cannot connect to %s Database: %s" % (db_type, db_location)))

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

current.db = db
from utility import formstyle_angular_material
## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ["*"]
## choose a style for forms
response.formstyle = formstyle_angular_material  # or 'bootstrap3_stacked' or 'bootstrap2' or other
#response.form_label_separator = get_app_settings("form_label_separator", "")
response.delimiters = ("<?","?>")

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager
import datetime, json

auth = Auth(db)
service = Service()
plugins = PluginManager()

## configure email
mail = auth.settings.mailer
login_email = get_app_settings("mail_login_email", "")
mail.settings.server = get_app_settings("mail_server", "logging")
mail.settings.sender = get_app_settings("mail_sender_email", None)
mail.settings.login = get_app_settings("mail_login", None)

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.formstyle = formstyle_angular_material

# END =========================================================================