# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from apps.messenger.views import MessengerWebhookView, MessengerRegister, MessengerLogin

from apps.messenger.views import facebook_account_linking

urlpatterns = [
    url(
        regex=r'^messenger/incomming/?$',
     	view=MessengerWebhookView.as_view(),
        name="view-messenger-validation"

    ),


    url(
        regex=r'^messenger/register/$',
        view=MessengerRegister.as_view(),
        name='view-messenger-register'
    ),

    url(
        regex=r'^messenger/login/$',
        view=MessengerLogin.as_view(),
        name='view-messenger-login'
    ),

    url(
        r'^facebook/authorize/(?P<uid>.*)/$',
        facebook_account_linking, 
        name="facebook_authorize"
    )
]