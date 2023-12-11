# Django-openid Testproject for University of Helsinki Login Service
This project is an example of a Django OpenID Connect configuration for University of Helsinki login service. The app connects to a test service and does not deal with any personal information of students or personnel.

# Configuration

## [pyproject.toml](https://github.com/ellaverak/django-openid/blob/main/pyproject.toml)

```authlib = "^1.2.1"```
Configuration base for the OpenID Connect client.

```django-environ = "^0.11.2"```
Add-on for environemnt variables.

```psycopg2 = "^2.9.9"```
This project uses a postgres database. The database connection is created with psycopg2.

```django-cryptography = "^1.1"```
Cryptography base for the postgres database.

## [settings.py](https://github.com/ellaverak/django-openid/blob/main/project/project/settings.py)

```LOGOUT_REDIRECT_URL = 'https://login-test.it.helsinki.fi/idp/profile/Logout'```

Defines the logout url as the University of Helsinki logout url.

```
AUTHLIB_OAUTH_CLIENTS = {
    'helsinki': {
        'client_id': os.getenv('OIDC_CLIENT_ID'),
        'client_secret': os.getenv('OIDC_CLIENT_SECRET')
    }
}```

Defines the name of the new OAUTH-client (helsinki) and sets the client_id and client_secret parameters. 

