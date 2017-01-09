# -*- coding: utf-8 -*-

from gluon import A, current, DIV, INPUT, LABEL, SELECT, SPAN, TAG, TEXTAREA
from pydal import Field

from datetime import datetime
import os
from uuid import uuid4

# =============================================================================
uuid_field = Field("uuid", notnull=True, unique=True,
                   length=128,
                   default=lambda:str(uuid4().urn),
                   readable=False,
                   writable=False,
                   )

deleted_field = Field("deleted", "boolean",
                      default=False,
                      readable=False,
                      writable=False,
                      )

deleted_fk_field = Field("deleted", "boolean",
                         default=False,
                         readable=False,
                         writable=False,
                         )

created_on_field = Field("created_on", "datetime",
                         default=datetime.utcnow(),
                         readable=False,
                         writable=False,
                         )

modified_on_field = Field("modified_on", "datetime",
                          default=datetime.utcnow(),
                          update=datetime.utcnow(),
                          readable=False,
                          writable=False,
                          )

# =============================================================================
def get_meta_fields_basic():

    return [uuid_field,
            deleted_field,
            deleted_fk_field,
            created_on_field,
            modified_on_field]

# =============================================================================
def get_meta_fields():


    auth = current.auth
    utable = auth.settings.table_user

    if auth.is_logged_in():
        # Not current.auth.user to support impersonation
        current_user = current.session.auth.user.id
    else:
        current_user = None

    created_by_field = Field("created_by", utable,
                             default=current_user,
                             requires=None,
                             readable=False,
                             writable=False,
                             ondelete="RESTRICT",
                             )

    modified_by_field = Field("modified_by", utable,
                              default=current_user,
                              update=current_user,
                              requires=None,
                              readable=False,
                              writable=False,
                              ondelete="RESTRICT",
                              )

    approved_by_field = Field("approved_by", utable,
                              requires=None,
                              readable=False,
                              writable=False,
                              )

    return [uuid_field,
            deleted_field,
            deleted_fk_field,
            created_on_field,
            modified_on_field,
            created_by_field,
            modified_by_field,
            approved_by_field]

# =============================================================================
def formstyle_angular_material(form, fields, *args, **kwargs):
    """
        Formstyle for Angular Material Theme
    """

    def render_row(row_id, label, widget, comment, hidden=False):

        input_container = TAG["md-input-container"](_class="md-block")
        input_append = input_container.append

        _class = "form-row row hide" if hidden else "form-row row"

        if isinstance(widget, (A, SPAN)):
            # Nothing to do; just add it
            if label:
                label.attributes["_style"] = "color:green"
                return DIV(label, widget, _class=_class, _id=row_id)
            else:
                return DIV(widget, _class=_class, _id=row_id)

        if isinstance(label, LABEL):
            label.attributes["_style"] = "color:green"
            input_append(label)

        if isinstance(widget, INPUT) and not isinstance(widget, SELECT):
            if "_type" in widget.attributes and \
               widget.attributes["_type"] == "checkbox":
                # Checkbox
                # Label contained here
                widget = TAG["md-checkbox"](label.components[0])
                return DIV(widget, _class=_class, _id=row_id)
            else:
                # Normal Input
                # Label contained above
                input_append(widget)

        if isinstance(widget, SELECT):
            # Get the options
            options = widget.components
            select = TAG["md-select"](**{"_ng-model": "dropdownSelect"})
            select_append = select.append
            for option in options:
                opt_attr = option.attributes
                select_append(TAG["md-option"](option.components[0],
                                               _value=opt_attr["_value"],
                                               _selected=opt_attr["_selected"]))
            input_append(select)

        if hasattr(widget, "element"):
            submit = widget.element("input", _type="submit")
            if submit:
                widget = TAG["md-button"](widget.attributes["_value"],
                                          _class="md-raised md-primary",
                                          _type="submit")
                return DIV(widget, _class=_class, _id=row_id)

        return DIV(input_container, _class=_class, _id=row_id)

    parent = TAG[""]()
    for row_id, label, widget, comment in fields:
        parent.append(render_row(row_id, label, widget, comment))
    return parent

# =============================================================================
def get_prepop_files():
    """ Return all the prepop file in the modules/ folder """

    prepop_files_path = current.app_settings["prepop_files_path"]

    prepop_files = os.listdir(prepop_files_path)

    return [prepop_file for prepop_file in prepop_files
            if prepop_file.endswith(".csv")]

# END =========================================================================