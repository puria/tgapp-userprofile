# -*- coding: utf-8 -*-
from hashlib import md5
import tg
from tg import url
from tgext.pluggable import app_model, plug_url
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tw2.core import Required
from tw2.forms import ListForm, TextField, TextArea, HiddenField,\
    FileField, SubmitButton, PasswordField
from formencode.validators import FieldsMatch


def get_profile_css(config):
    return url(config['_pluggable_userprofile_config'].get(
        'custom_css', '/_pluggable/userprofile/css/style.css'))


def _get_user_gravatar(email_address):
    if not isinstance(email_address, bytes):
        email_address = email_address.encode('utf-8')
    mhash = md5(email_address).hexdigest()
    return url('http://www.gravatar.com/avatar/'+mhash, params=dict(s=32))


def get_user_data(user):
    user_data = getattr(user, 'profile_data', {'display_name': (l_('Display Name'), user.display_name),
                                               'email_address': (l_('Email Address'), user.email_address)})

    user_avatar = user_data.pop('avatar', None)
    if user_avatar is None:
        fbauth_info = getattr(user, 'fbauth', None)
        if fbauth_info is not None:
            user_avatar = fbauth_info.profile_picture + '?type=large'
        else:
            user_avatar = _get_user_gravatar(user_data['email_address'][1])

    return user_data, user_avatar


def update_user_data(user, user_data):
    for k, v in user_data.items():
        setattr(user, k, v)


class UserForm(ListForm):
    uid = HiddenField()
    submit = SubmitButton(value=l_('Save'))


def create_user_form(user):
    profile_form = getattr(user, 'profile_form', None)
    if not profile_form:
        user_data, user_avatar = get_user_data(user)
        profile_form = UserForm()

        for name, info in user_data.items():
            profile_form.child = profile_form.child()
            profile_form.child.children.append(TextField(id=name, validator=Required, label=info[0]))

        profile_form = profile_form()
    return profile_form


class ChangePasswordForm(ListForm):
    password = PasswordField(label=u'Password', validator=Required)
    verify_password = PasswordField(label=l_(u'Confirm Password'), validator=Required)
    submit = SubmitButton(value=l_('Save'))
    validator = FieldsMatch('password', 'verify_password',
                            messages={'invalidNoMatch': l_('Passwords do not match')})


def create_change_password_form():
    return ChangePasswordForm()
