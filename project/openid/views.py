import json
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth

CONF_URL = 'https://login-test.it.helsinki.fi/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='helsinki',
    server_metadata_url=CONF_URL,
    userinfo_endpoint='https://login-test.it.helsinki.fi/idp/profile/oidc/userinfo',
    client_kwargs={
        'scope': 'openid profile'
    }
)


def home(request):
    return HttpResponse("Home")


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.helsinki.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.helsinki.authorize_access_token(request)
#    user = request.session['user'] = token['userinfo']
#    mail = request.session['email'] = token['userinfo']
    user = oauth.helsinki.userinfo(token=token)
    print(user)
#    print(mail)
    return redirect('/')
