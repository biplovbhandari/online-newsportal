# -*- coding: utf-8 -*-

from utility import formstyle_angular_material

get_app_settings = app_settings.get

# -----------------------------------------------------------------------------
# Languages

# Default strings are in US English
T.current_languages = ("en", "en-us")
# Check if user has selected a specific language
if get_vars._language:
    language = get_vars._language
elif session.language:
    # Use the last-selected language
    language = session.language
elif auth.is_logged_in():
    # Use user preference
    language = auth.user.language
else:
    # Use system default
    language = get_app_settings("l10n_default_language", "en")
#else:
#    # Use what browser requests (default web2py behaviour)
#    T.force(T.http_accept_language)

# IE doesn't set request.env.http_accept_language
#if language != "en":
T.force(language)

# -----------------------------------------------------------------------------
# Auth

_settings = auth.settings
_settings.lock_keys = False

_settings.expiration = 28800 # seconds

# Require Email Verification
_settings.registration_requires_verification = get_app_settings(\
                            "auth_registration_requires_verification", False)

# Require Admin approval for self-registered users
_settings.registration_requires_approval = get_app_settings(\
                                "auth_registration_requires_approval", False)

_settings.reset_password_requires_verification = get_app_settings(\
                            "auth_reset_password_requires_verification", True)
_settings.on_failed_authorization = URL(c="default",
                                        f="user",
                                        args="not_authorized")
_settings.verify_email_next = URL(c="default", f="index")

# We don't wish to clutter the groups list with 1 per user.
_settings.create_user_groups = False
# We need to allow basic logins for Webservices
_settings.allow_basic_login = True

# formstyle
_settings.formstyle = formstyle_angular_material

_settings.lock_keys = True

# -----------------------------------------------------------------------------
# Mail

_mail_settings = mail.settings
_mail_settings.server = get_app_settings("mail_server", "logging")
_mail_settings.sender = get_app_settings("mail_sender_email", None)
_mail_settings.login = get_app_settings("mail_login", None)

# -----------------------------------------------------------------------------
# Response

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ["*"]
## choose a style for forms
response.formstyle = formstyle_angular_material  # or 'bootstrap3_stacked' or 'bootstrap2' or other
#response.form_label_separator = get_app_settings("form_label_separator", "")
response.delimiters = ("<?", "?>")

# END =========================================================================
