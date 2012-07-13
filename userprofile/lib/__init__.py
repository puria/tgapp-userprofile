# -*- coding: utf-8 -*-

from tg import url
from tgext.pluggable import app_model, plug_url

from tw.forms import ListForm, TextField
from tw.forms.validators import UnicodeString

def get_profile_css(config):
    return url(config['_pluggable_userprofile_config'].get('custom_css',
                                                           '/_pluggable/userprofile/css/style.css'))

def get_user_data(user):
    user_data = getattr(user, 'profile_data', {'display_name':('Display Name', user.display_name),
                                               'email_address':('Email Address', user.email_address)})

    user_avatar = user_data.pop('avatar', None)
    if user_avatar is None:
        fbauth_info = getattr(user, 'fbauth', None)
        if fbauth_info is not None:
            user_avatar = fbauth_info.profile_picture + '?type=large'
        else:
            user_avatar = url('/_pluggable/userprofile/images/default_avatar.jpg')

    return user_data, user_avatar

def update_user_data(user, user_data):
    for k, v in user_data.items():
        setattr(user, k, v)

def create_user_form(user):
    profile_form = getattr(user, 'profile_form', None)
    if not profile_form:
        user_data, user_avatar = get_user_data(user)
        form_fields = [TextField(id=name, validator=UnicodeString(not_empty=True),
                                 label_text=info[0]) for name, info in user_data.items()]
        profile_form = ListForm(fields=form_fields, submit_text='Save',
                                action=plug_url('userprofile', '/save'))
    return profile_form

