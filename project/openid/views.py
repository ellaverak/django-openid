import json
import environ, os
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from authlib.integrations.django_client import OAuth

env = environ.Env()
environ.Env.read_env()

CONF_URL = env('OIDC_REDIRECT_URI')
oauth = OAuth()
oauth.register(
    name='helsinki',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid profile email'}
)


def home_page_view(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user)
    return render(request, 'home.html', context={'user': user})
#    return HttpResponse("Hello world!")

def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))
    return oauth.helsinki.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.helsinki.authorize_access_token(request)
    request.session['user'] = token['userinfo']
    return redirect('/')


def logout(request):
    request.session.pop('user', None)
    return redirect('/')