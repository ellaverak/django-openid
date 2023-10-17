import environ
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from authlib.integrations.requests_client import OAuth2Session

env = environ.Env()
environ.Env.read_env()

client_id = env("OIDC_CLIENT_ID")
client_secret = env("OIDC_CLIENT_SECRET")
authorization_endpoint = env("OIDC_REDIRECT_URI")
scope = "openid profile"

client = OAuth2Session(client_id, client_secret, scope=scope)

def home(request):
    return HttpResponse("Home")

def login(request):
    uri, state = client.create_authorization_url(authorization_endpoint)
    return redirect(uri)