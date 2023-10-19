import json
import urllib.parse
import requests
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
        'scope': 'openid'
    }
)

claims_data = {
        "id_token": {
            "hyPersonStudentId": { "essential": True },
            "uid": None
        },
        "userinfo": {
            "email": { "essential": True },
            "family_name": { "essential": True },
            "given_name": { "essential": True },
            "hyGroupCn": None,
            "hyPersonStudentId": { "essential": True },
            "uid": None
        }
    }

claims = json.dumps(claims_data)

def home(request):
    return HttpResponse("Home")


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.helsinki.authorize_redirect(request, redirect_uri, claims=claims)


def auth(request):
    #fetch access token
    token = oauth.helsinki.authorize_access_token(request)

    #use access token to access the userinfo endpoint via openid connect
    user = oauth.helsinki.userinfo(token=token) #tällä saa uid eli tunnus, givenname, surname, email!

    #userinfo returns userinfo claims as a dictionary. For example: uid, given_name, family_name, email
    print(user)

    code = request.GET.get('code')
    id_token = oauth.helsinki.fetch_token(code=code)
    print(id_token)

    return redirect('/')
