import json

import requests

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q

from apps.contrib.format.strings import get_uuid
from apps.messenger.components.client import MessengerClient
from apps.messenger.delivery.conversation import generate_response

from apps.users.models import User

from apps.messenger.components.webhooks import Webhook

from apps.messenger.models import MessengerSession, MessengerInfo, Intent


PAGE_ACCESS_TOKEN ='EAAPjZCQiYrM8BAOJy44zzJoHLegIIiPNgwVoDnMxfNJgRHmEKcUkLUZAndqZAW6NZBJhxhUsDREUfkqHewR1q4fNIP2UNJof0F89uj2uvn5TRXGlcf019MYDUJpJmizOTEhE8UzgmiYA7Spi5d3G0DEoH8ZCfMTjDkBVv4vbU3gZDZD'

from constance import config


class MessengerWebhookView(View):
    messenger = MessengerClient(access_token=config.PAGE_ACCESS_TOKEN)

    def get(self, request, *args, **kwargs):

        if request.GET['hub.verify_token'] == config.VALIDATION_CODE:
            print("\n ------->>> Webhook vinculado!!")
            return HttpResponse(request.GET['hub.challenge'])
        else:
            print("\n ------->>> Webhook Error!!")

            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        payload = json.loads(request.body.decode('utf-8'))

        # print("\n\n\>>>>>>>>>>>>>>>>>>>>>>\n", payload, "\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n\n")

        webhook = Webhook(payload)

        for entry in webhook.entries:
            for event in entry.messaging:
                generate_response(event, self.messenger)
                
        return HttpResponse(status=200)


class MessengerMixin(object):
    def get_context_data(self, **kwargs):
        context = super(MessengerMixin, self).get_context_data(**kwargs)
        context["messenger"] = True
        return context


class MessengerRegister(MessengerMixin, TemplateView):
    template_name = "account/signup.html"

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect('/messenger/register/')


def get_messenger_session(user, uid, page_id, psid):
    has_linking = MessengerInfo.objects.filter(user=user, messenger_id=uid).exists()
    if has_linking:
        link = MessengerInfo.objects.get(user=user, messenger_id=uid)
        link.user = user

    else:
        link = MessengerInfo(
            user=user,
            messenger_id=uid
        )
    link.save()
    has_session = MessengerSession.objects.filter(psid=psid).exists()

    if has_session:
        session = MessengerSession.objects.get(psid=psid)
    else:
        user_session = MessengerInfo.objects.get(user=user)

        session = MessengerSession(
            info=user_session,
            page_id=page_id,
            token=get_uuid(),
            psid=psid
        )
        session.save()
    return session


class MessengerLogin(MessengerMixin, TemplateView):

    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):

        login = request.POST.get("login", None)
        password = request.POST.get("password", None)

        redirect_uri = request.POST.get("redirect_uri", None)
        page_id = request.POST.get("page_id", None)
        psid = request.POST.get("psid", None)
        uid = request.POST.get("uid", None)

        print("\n\n REDIRECT_URI", redirect_uri, "\n\n")
        print("\n\n PAGE_ID",page_id, "\n\n")
        print("\n\n PSID",psid, "\n\n")
        print("\n\n UID",uid, "\n\n")

        if login and password:
            user_exist = User.objects.filter(Q(username=login) | Q(email=login)).exists()

            print("\n\n EXISTEN USER Y PASS", "\n\n")

            if user_exist:
                user = User.objects.get(Q(username=login) | Q(email=login))
                valid_pass = user.check_password(password)

                print("\n\n USUARIO VALIDA", "\n\n")

                if valid_pass:
                    session = get_messenger_session(user, uid, page_id, psid)

                    print("\n\n CONTRASEÑA VALIDA", "\n\n")

                    if redirect_uri:

                        print("\n\n TODO VALIDOOOOOO", "\n\n")

                        return send_messenger_token(request, session, redirect_uri)
        else:
            return HttpResponseRedirect('/messenger/login/')


def send_messenger_token(request, session=None, redirect_uri=None):
    if redirect_uri:
        new_uri = redirect_uri + "&authorization_code=" + session.token
        print("Redirigiendo a Facebook")

        response = requests.get(new_uri)

        return redirect(new_uri, permanent=True)

    return redirect("facebook_authorize", permanent=True)


def facebook_account_linking(request, uid):
    messenger = MessengerClient(access_token=config.PAGE_ACCESS_TOKEN)
    account_linking_token = request.GET.get('account_linking_token', None)
    redirect_uri = request.GET.get('redirect_uri', None)

    page_id, psid = messenger.get_psid(alt=account_linking_token)
    has_linking = MessengerSession.objects.filter(psid=psid).exists()

    if has_linking:

        link = MessengerSession.objects.get(psid=psid)
        user = link.user
        session = get_messenger_session(user, uid, page_id, psid)
        return send_messenger_token(request ,session, redirect_uri)

    else:
        ctx = {
            "redirect_uri": redirect_uri,
            "page_id": page_id,
            "psid": psid,
            "messenger": True,
            "uid": uid
        }
        return render(request, 'account/login.html', ctx )
