# Django-openid Testproject for University of Helsinki Login Service
This project is an example of a Django OpenID Connect configuration for University of Helsinki login service. The app connects to a test service and does not deal with any personal information of students or personnel.

# The Basics

OpenID Connect is an identity layer built on top of the OAuth 2.0 framework. OpenID Connect is based on configuration data that is openly awailable and can be read by the OAuth-client. For example the configuration data for the University of Helsinki login (test) service can be found from https://login-test.it.helsinki.fi/.well-known/openid-configuration

The OAuth-client is set up using the configuration data. The Client communicates with the University of Helsinki sp-registry service responsible for distibuting user data. User data can be reached via an userinfo endpoint or it can be decoded from an id_token.

# Configuration

## [pyproject.toml](https://github.com/ellaverak/django-openid/blob/main/pyproject.toml)

```authlib = "^1.2.1"```
Configuration base for the OpenID Connect client (OAuth-client).

```django-environ = "^0.11.2"```
Add-on for environemnt variables.

```psycopg2 = "^2.9.9"```
This project uses a postgres database. The database connection is created with psycopg2.

```django-cryptography = "^1.1"```
Cryptography base for the postgres database.

## [settings.py](https://github.com/ellaverak/django-openid/blob/main/project/project/settings.py)

```
LOGOUT_REDIRECT_URL = 'https://login-test.it.helsinki.fi/idp/profile/Logout'
```

Defines the logout url as the University of Helsinki logout url.

```
AUTHLIB_OAUTH_CLIENTS = {
    'helsinki': {
        'client_id': os.getenv('OIDC_CLIENT_ID'),
        'client_secret': os.getenv('OIDC_CLIENT_SECRET')
    }
}
```

Defines the name of the new OAuth-client (helsinki) and sets the client_id and client_secret parameters. The parameter values can be found from the University of Helsinki sp-registry.

## [views.py](https://github.com/ellaverak/django-openid/blob/main/project/openid/views.py)

```import urllib.request, json```
Keyset for decoding userdata from the id_token is in json format.

```from django.contrib.auth import authenticate as django_authenticate```

```from django.contrib.auth import login as django_login```
Django's inbuild functions are importent with custom names to avoid conflict with the view-function names.

```from authlib.integrations.django_client import OAuth```
OAuth-client.

```from authlib.oidc.core import CodeIDToken```
CodeIDToken includes the instructions for decoding the id_token.

```from authlib.jose import jwt```
Used for transferring claims between the OAuth-client and the corresponding service.

```
CONF_URL = 'https://login-test.it.helsinki.fi/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='helsinki',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid profile'
    }
)
```

Registers the OAuth-client (helsinki) using the openid-configuration.

```
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
```

Defines the claims that OAuth-client requests from the service.

```
with urllib.request.urlopen("https://login-test.it.helsinki.fi/idp/profile/oidc/keyset") as url:
    keys = json.load(url)
```









