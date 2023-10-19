import urllib.request, json
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt


CONF_URL = 'https://login-test.it.helsinki.fi/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='helsinki',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid profile'
    }
)

claims_data = {
        "id_token": {
            "uid": None
        },
        "userinfo": {
            "email": None,
            "family_name": None,
            "given_name": None,
            "hyGroupCn": None,
            "hyPersonStudentId": None,
            "uid": None
        }
    }

claims = json.dumps(claims_data)

with urllib.request.urlopen("https://login-test.it.helsinki.fi/idp/profile/oidc/keyset") as url:
    keys = json.load(url)


def home(request):
    return HttpResponse("Home")


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.helsinki.authorize_redirect(request, redirect_uri, claims=claims)


def auth(request):
    #fetch token
    token = oauth.helsinki.authorize_access_token(request)

    #token is a dictionary including the access_token, id_token etc.
    #print(token)
    #print(token['access_token'])
    #print(token['id_token'])

    #use tokens to access the userinfo endpoint via openid connect
    userinfo = oauth.helsinki.userinfo(token=token)

    #userinfo returns userinfo claims as a dictionary. For example: uid, given_name, family_name, email
    #print(userinfo)

    claims = jwt.decode(token['id_token'], keys, claims_cls=CodeIDToken)
    claims.validate()
    print(claims)

    #id_token = oauth.helsinki.fetch_token(code=code)
    #print(id_token)

    return redirect('/')
