# -*- coding: utf-8 -*-

from gluon import current
from gluon.html import *
from gluon.storage import Storage
from gluon.tools import Auth
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_IN_DB, IS_NOT_IN_DB, CRYPT

from pydal import Field

from utility import get_meta_fields_basic, get_meta_fields

DEFAULT = lambda: None

# =============================================================================
class Authentication(Auth):

    """
        customisation of the gluon.tools.Auth class

        - override:
            - __init__
            - define_tables

    """

    SYSTEM_ROLES = ["ADMIN", "AUTHENTICATED", "ANONYMOUS", "EDITOR"]

    def __init__(self):

        """ Initialise parent class & make any necessary modifications """

        Auth.__init__(self, current.db)

        T = current.T

        self.settings.lock_keys = False
        self.settings.login_userfield = "email"
        #self.settings.db_methods = {"CREATE"  : T("Create"),
        #                            "READ"    : T("Read"),
        #                            "UPDATE"  : T("UPDATE"),
        #                            "DELETE"  : T("DELETE"),
        #                            #"PUBLISH" : T("Publish"),
        #                            #"APPROVE" : T("Approve")
        #                            }

        self.settings.lock_keys = True

        messages = self.messages
        messages.lock_keys = False

        messages.email_sent = "Verification Email sent - please check your email to validate. If you do not receive this email please check you junk email or spam filters"
        messages.email_verified = "Email verified - you can now login"
        messages.label_remember_me = "Remember Me"
        messages.password_reset_button = "Request password reset"
        messages.registration_verifying = "You haven't yet Verified your account - please check your email"
        messages.reset_password = "Click on the link %(url)s to reset your password"
        messages.verify_email = "Click on the link %(url)s to verify your email"
        messages.verify_email_subject = "%(system_name)s - Verify Email"
        messages.welcome_email_subject = "Welcome to %(system_name)s"
        messages.welcome_email = \
"""Welcome to %(system_name)s
 - You can start using %(system_name)s at: %(url)s
 - To edit your profile go to: %(url)s%(profile)s
Thank you"""
        messages.lock_keys = True

        # Permissions
        self.permission = Permission(self)

    # -------------------------------------------------------------------------
    def define_tables(self, migrate=True, fake_migrate=False):
        """
        To be called unless tables are defined manually

        Examples:
            Use as::

                # defines all needed tables and table files
                # 'myprefix_auth_user.table', ...
                auth.define_tables(migrate='myprefix_')

                # defines all needed tables without migration/table files
                auth.define_tables(migrate=False)

        """

        db = current.db
        settings = self.settings
        messages = self.messages
        app_settings = current.app_settings
        define_table = db.define_table

        # User table
        utable = settings.table_user
        uname = settings.table_user_name
        if not utable:
            utable_fields = [
                Field("first_name", length=128, notnull=True,
                      default = "",
                      requires = \
                      IS_NOT_EMPTY(error_message=messages.is_empty),
                      ),
                Field("middle_name", length=128,
                      default = ""),
                Field("last_name", length=128,
                      default = ""),
                Field("email", length=255, unique=True,
                      default = "",
                      requires = [IS_EMAIL(error_message=messages.invalid_email),
                                  IS_NOT_IN_DB(db, "%s.email" % settings.table_user_name,
                                               error_message=messages.email_taken)
                                  ]
                      ),
                Field(settings.password_field, "password", length=512,
                      requires=CRYPT(key=settings.hmac_key,
                                     min_length=app_settings["password_min_length"],
                                     digest_alg="sha512"),
                      readable=False,
                      label=messages.label_password),
                # @ToDo: allow login with username when required
                Field("username", length=128, default="",
                      readable=False, writable=False),
                Field("language",length=16,
                      readable=False, writable=False),
                Field("utc_offset", length=16,
                      readable=False, writable=False),
                Field("registration_key", length=512,
                      default="",
                      readable=False, writable=False),
                Field("reset_password_key", length=512,
                      default="",
                      readable=False, writable=False),
                ]
            utable_fields += list(get_meta_fields_basic())

            define_table(uname,
                         migrate = migrate,
                         fake_migrate = fake_migrate,
                         *utable_fields)
            utable = settings.table_user = db[uname]

        # Group table (roles)
        gtable = settings.table_group
        gname = settings.table_group_name
        if not gtable:
            define_table(gname,
                # Role name:
                Field("role", length=255, unique=True,
                      default="",
                      requires = IS_NOT_IN_DB(db, "%s.role" % gname),
                      label=messages.label_role),
                Field("description", "text",
                      label=messages.label_description),
                Field("hidden", "boolean",
                      readable=False, writable=False,
                      default=False),
                *get_meta_fields(),
                migrate = migrate,
                fake_migrate = fake_migrate
                )
            gtable = settings.table_group = db[gname]

        # Group membership table (user<->role)
        if not settings.table_membership:
            define_table(
                settings.table_membership_name,
                Field("user_id", utable,
                      requires = IS_IN_DB(db, "%s.id" % uname,
                                          "%(id)s: %(first_name)s %(last_name)s"),
                      label=messages.label_user_id),
                Field("group_id", gtable,
                      requires = IS_IN_DB(db, "%s.id" % gname,
                                          "%(id)s: %(role)s"),
                      label=messages.label_group_id),
                *get_meta_fields(),
                migrate = migrate,
                fake_migrate = fake_migrate
                )
            settings.table_membership = db[settings.table_membership_name]

        # Permission table
        self.permission.define_table(migrate=migrate,
                                     fake_migrate=fake_migrate)

        # Event table (auth_event)
        if not settings.table_event:
            request = current.request
            define_table(
                settings.table_event_name,
                Field("time_stamp", "datetime",
                      default=request.utcnow,
                      #label=messages.label_time_stamp
                      ),
                Field("client_ip",
                      default=request.client,
                      #label=messages.label_client_ip
                      ),
                Field("user_id", utable, default=None,
                      requires = IS_IN_DB(db, "%s.id" % uname,
                                          "%(id)s: %(first_name)s %(last_name)s"),
                      #label=messages.label_user_id
                      ),
                Field("origin", default="auth", length=512,
                      #label=messages.label_origin,
                      requires = IS_NOT_EMPTY()),
                Field("description", "text", default="",
                      #label=messages.label_description,
                      requires = IS_NOT_EMPTY()),
                *get_meta_fields(),
                migrate = migrate,
                fake_migrate=fake_migrate
                )
            settings.table_event = db[settings.table_event_name]

    # -------------------------------------------------------------------------
    def check_group(self):
        """
            Check if any group is present in the system

            @return True if present else False
        """

        table = self.settings.table_group

        record = current.db(table.deleted!=True).select(table.id,
                                                        limitby=(0, 1)
                                                        ).first()
        if record:
            return True

        return False

    # -------------------------------------------------------------------------
    def create_system_group(self):
        """
            Create System User Groups
        """

        group_id = []
        for _role in self.SYSTEM_ROLES:
            _role_id = self.add_group(_role)
            group_id.append(_role_id)

        return group_id

    # -------------------------------------------------------------------------
    def create_or_update_group(self, group, description=None, hidden=False, *rules):
        """
            Create or update group
        """

        table = current.auth.settings.table_group
        query = (table.role == group) & (table.deleted != True)
        record = current.db(query).select(table.id, limitby=(0, 1)).first()
        if record:
            group_id = record.id
            record.update_record(deleted=False,
                                 role=group,
                                 description=description,
                                 hidden=hidden)
        else:
            group_id = table.insert(role=group,
                                    description=description,
                                    hidden=hidden)
        if group_id:
            for rule in rules:
                self.permission.update_acl(group_id, **rule)

        return group_id

# =============================================================================
class Permission(object):
    """ Class to handle permissions """

    METHODS = Storage({
        "create"  : "CREATE",
        "read"    : "READ",
        "update"  : "UPDATE",
        "delete"  : "DELETE",
        "review"  : "REVIEW",
        "publish" : "PUBLISH",
    })

    # -------------------------------------------------------------------------
    def __init__(self, auth):
        """ Constructor """

        db = current.db

        # Instantiated once per request, but before Auth tables
        # are defined and authentication is checked, thus no use
        # to check permissions in the constructor

        # Store auth reference in self because current.auth is not
        # available at this point yet, but needed in define_table.
        self.auth = auth

        # table
        self.table = auth.settings.table_permission
        self.tablename = auth.settings.table_permission_name

        # Error messages
        T = current.T
        self.INSUFFICIENT_PRIVILEGES = T("Insufficient Privileges")
        self.AUTHENTICATION_REQUIRED = T("Authentication Required")

        # Request information
        request = current.request
        self.controller = request.controller
        self.function = request.function

        # Default landing pages
        _next = URL(args=request.args, vars=request.get_vars)
        self.homepage = URL(c="default", f="index")
        self.loginpage = URL(c="default", f="user", args="login",
                             vars=dict(_next=_next))

    # -------------------------------------------------------------------------
    def define_table(self, migrate=True, fake_migrate=False):
        """
            Define permission table, invoked by Authentication.define_tables()
        """

        auth = self.auth
        messages = auth.messages
        if not self.table:
            db = current.db
            db.define_table(
                self.tablename,
                Field("group_id", auth.settings.table_group,
                      label=messages.label_group_id),
                #Field("name", default="default", length=512,
                #      label=messages.label_name,
                #      requires=IS_NOT_EMPTY(error_message=messages.is_empty)),
                Field("controller", length=64),
                Field("function", length=512),
                Field("tablename", length=512,
                      label=messages.label_table_name),
                Field("record_id", "integer"),
                Field("user_create", "boolean",
                      default=False,
                      ),
                Field("user_read", "boolean",
                      default=False,
                      ),
                Field("user_update", "boolean",
                      default=False,
                      ),
                Field("user_delete", "boolean",
                      default=False,
                      ),
                Field("owner_create", "boolean",
                      default=False,
                      ),
                Field("owner_read", "boolean",
                      default=False,
                      ),
                Field("owner_update", "boolean",
                      default=False,
                      ),
                Field("owner_delete", "boolean",
                      default=False,
                      ),
                *get_meta_fields(),
                migrate = migrate,
                fake_migrate = fake_migrate
                )
            self.table = db[self.tablename]

    # -------------------------------------------------------------------------
    def update_acl(self, group,
                   controller=None,
                   function=None,
                   tablename=None,
                   user_create=False,
                   user_read=False,
                   user_update=False,
                   user_delete=False,
                   owner_create=False,
                   owner_read=False,
                   owner_update=False,
                   owner_delete=False):

        table = self.table

        if not table:
            return None

        if controller is None and function is None and tablename is None:
            return None

        if tablename is not None:
            controller = function = None

        success = False

        if group:
            group_id = None
            acl = dict(group_id=group_id,
                       deleted=False,
                       controller=controller,
                       function=function,
                       tablename=tablename,
                       user_create=user_create,
                       user_read=user_read,
                       user_update=user_update,
                       user_delete=user_delete,
                       owner_create=owner_create,
                       owner_read=owner_read,
                       owner_update=owner_update,
                       owner_delete=owner_delete)
            if isinstance(group, basestring) and not group.isdigit():
                gtable = self.auth.settings.table_group
                query = (gtable.role == group) & (table.group_id == gtable.id)
            else:
                query = (table.group_id == group)
                group_id = group

            query &= ((table.controller == controller) & \
                      (table.function == function) & \
                      (table.tablename == tablename))
            record = current.db(query).select(table.id,
                                              table.group_id,
                                              limitby=(0, 1)).first()
            if record:
                acl["group_id"] = record.group_id
                record.update_record(**acl)
                success = record.id
            elif group_id:
                acl["group_id"] = group_id
                success = table.insert(**acl)
            else:
                # Lookup the group_id
                record = current.db(gtable.group == group).select(gtable.id,
                                                                  limitby=(0, 1)
                                                                  ).first()
                if record:
                    acl["group_id"] = group_id
                    success = table.insert(**acl)

        return success

# END =========================================================================
