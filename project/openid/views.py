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
    #token ="1223"
    #headers = {"Authorization": f"Token {token}"}
    #url = "https://userinfo"
    #requests.post(url, headers==headers)
    return HttpResponse("Home")



def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.helsinki.authorize_redirect(request, redirect_uri, claims=claims)


def auth(request):
    token = oauth.helsinki.authorize_access_token(request)
    print(token)

    headers = {"Authorization": f"Token {token}"}
    url = "https://login-test.it.helsinki.fi/idp/profile/oidc/userinfo"
    userinfo = requests.post(url, headers=headers)
    print(userinfo)

    family_name = request.session['family_name'] = token['userinfo']
    print(family_name)

    user = oauth.helsinki.userinfo(token=token)
    print(user)
    return redirect('/')
