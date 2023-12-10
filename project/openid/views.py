import urllib.request, json
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from authlib.integrations.django_client import OAuth
from authlib.oidc.core import CodeIDToken
from authlib.jose import jwt


#register openidconnect client
CONF_URL = 'https://login-test.it.helsinki.fi/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='helsinki',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid profile'
    }
)

#claims are provided to the authorization endpoint
claims_data = {
        "id_token": {
            "hyPersonStudentId": None

        },
        "userinfo": {
            "email": None,
            "family_name": None,
            "given_name": None,
            "uid": None
        }
    }

claims = json.dumps(claims_data)

#keyset for decoding the id_token
with urllib.request.urlopen("https://login-test.it.helsinki.fi/idp/profile/oidc/keyset") as url:
    keys = json.load(url)


@login_required
def home(request):
    return render(request, "home.html")


def login(request):
    #build redirect_uri
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    #authorize and provide claims
    return oauth.helsinki.authorize_redirect(request, redirect_uri, claims=claims)


def auth(request):
    #fetch token
    token = oauth.helsinki.authorize_access_token(request)

    #token is a dictionary including the access_token, id_token etc.

    #use tokens to access the userinfo endpoint via openid connect
    userinfo = oauth.helsinki.userinfo(token=token)

    #userinfo returns userinfo claims as a dictionary. For example: uid, given_name, family_name, email

    #decode id_token
    userdata = jwt.decode(token['id_token'], keys, claims_cls=CodeIDToken)
    userdata.validate()

    #id_token includes user information (and other info), but the id_token is more highly secured than the userinfo at userendpoint

    user = django_authenticate(userinfo=userinfo, userdata=userdata)
    if user is not None:
        django_login(request, user)

    return redirect(home)
