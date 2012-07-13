# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPNotFound

try:
    from repoze.what import predicates
except ImportError:
    from tg import predicates

from userprofile.model import DBSession
from userprofile.lib import create_user_form, get_user_data, get_profile_css, update_user_data
from tgext.pluggable import app_model, plug_url, primary_key

class RootController(TGController):
    @expose('userprofile.templates.index')
    def default(self, uid):
        user = DBSession.query(app_model.User).filter(primary_key(app_model.User)==uid).first()
        if not user:
            raise HTTPNotFound()

        user_data, user_avatar = get_user_data(user)
        user_displayname = user_data.pop('display_name', (None, 'Unknown'))
        user_partial = config['_pluggable_userprofile_config'].get('user_partial')

        return dict(user=user, is_my_own_profile=request.identity and request.identity['user'] == user,
                    user_data=user_data, user_avatar=user_avatar,
                    user_displayname=user_displayname,
                    profile_css=get_profile_css(config),
                    user_partial=user_partial)

    @expose('userprofile.templates.edit')
    @require(predicates.not_anonymous())
    def edit(self):
        user = request.identity['user']
        user_data, user_avatar = get_user_data(user)
        user_data = dict([(fieldid, info[1]) for fieldid, info in user_data.items()])
        return dict(user=user_data, profile_css=get_profile_css(config),
                    user_avatar=user_avatar,
                    form=create_user_form(user))

    @expose()
    @require(predicates.not_anonymous())
    def save(self, **kw):
        user = request.identity['user']
        profile_save = getattr(user, 'save_profile', None)
        if not profile_save:
            profile_save = update_user_data
        profile_save(user, kw)
        return redirect(plug_url('userprofile', '/%s' % getattr(user, primary_key(app_model.User).name)))