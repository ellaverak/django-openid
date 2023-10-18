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
    client_kwargs={
        'scope': 'openid profile'
    }
)


def home(request):
    return HttpResponse("Home")


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    print(redirect_uri)
    return oauth.helsinki.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.helsinki.authorize_access_token(request)
    request.session['user'] = token['userinfo']
    return redirect('/')
