import urllib.request, json
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
            "email": None,
            "given_name": None,
            "uid": None

        },
        "userinfo": {
            "email": None,
            "family_name": None,
            "hyGroupCn": None,
            "hyPersonStudentId": None,
            "uid": None
        }
    }

claims = json.dumps(claims_data)

#keyset for decoding the id_token
with urllib.request.urlopen("https://login-test.it.helsinki.fi/idp/profile/oidc/keyset") as url:
    keys = json.load(url)


def home(request):
    print(request.session.get('userinfo'))
    print(request.session.get('userdata'))

#   if request.user.is_authenticated:
#        print("toimii")

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
    #claims are presented as a dictionary

#    request.session['userinfo'] = userinfo
#    request.session['userdata'] = data

    user = authenticate(userinfo=userinfo)
    if user is not None:
        print('TEST')
#        login(user)

    return redirect(home)

def logout(request):
    logout(request)

    #logout
    return redirect("https://login-test.it.helsinki.fi/idp/profile/Logout")
