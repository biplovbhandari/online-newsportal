# -*- coding: utf-8 -*-

from gluon import current
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
        if not settings.table_permission:
            define_table(
                settings.table_permission_name,
                Field("group_id", gtable,
                      label=messages.label_group_id),
                #Field("name", default="default", length=512,
                #      label=messages.label_name,
                #      requires=IS_NOT_EMPTY(error_message=messages.is_empty)),
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
            settings.table_permission = db[settings.table_permission_name]

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
    def check_role(self):
        """
            Check if any role is present in the system

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
    def create_system_role(self):
        """
            Create System User Groups
        """

        table = self.settings.table_group

        role_id = []
        for _role in self.SYSTEM_ROLES:
            _role_id = table.insert(role=_role)
            role_id.append(_role_id)

        return role_id

# END =========================================================================
