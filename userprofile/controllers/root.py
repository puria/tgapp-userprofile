# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPNotFound

from userprofile import model
from userprofile.model import DBSession
from amolamusica.model.auth import User

from tgext.pluggable import plug_url

class RootController(TGController):
    @expose('userprofile.templates.index')
    def default(self, uid):
        user = DBSession.query(User).filter_by(user_id=uid).first()
        if not user:
            raise HTTPNotFound()

        user_data = getattr(user, 'profile_data', {'display_name':user.display_name,
                                                   'Username':user.user_name, 
                                                   'Email Address':user.email_address})

        user_displayname = user_data.pop('display_name', 'Unknown')

        user_avatar = user_data.pop('avatar', None)
        if user_avatar is None:
            fbauth_info = getattr(user, 'fbauth', None)
            if fbauth_info is not None:
                user_avatar = fbauth_info.profile_picture + '?type=large'
            else:
                user_avatar = url('/_pluggable/userprofile/images/default_avatar.jpg')

        profile_css = url(config['_pluggable_userprofile_config'].get('custom_css',
                                                                      '/_pluggable/userprofile/css/style.css'))

        user_partial = config['_pluggable_userprofile_config'].get('user_partial')

        return dict(user_data=user_data, user_avatar=user_avatar, user_displayname=user_displayname,
                    profile_css=profile_css, user_partial=user_partial)
