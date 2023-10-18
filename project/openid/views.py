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
    auth_url = 'https://login-test.it.helsinki.fi/idp/profile/oidc/authorize'
    return oauth.helsinki.authorize_redirect(request, auth_url)