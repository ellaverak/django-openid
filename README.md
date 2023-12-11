# Django-openid Testproject for University of Helsinki Login Service
This project is an example of a Django OpenID Connect configuration for University of Helsinki login service. The app connects to a test service and does not deal with any personal information of students or personnel.

# Configuration

## [settings.py](https://github.com/ellaverak/django-openid/blob/main/project/project/settings.py)

```LOGOUT_REDIRECT_URL = 'https://login-test.it.helsinki.fi/idp/profile/Logout'```

Defines the logout url as a University of Helsinki logout url.



```
AUTHLIB_OAUTH_CLIENTS = {
    'helsinki': {
        'client_id': os.getenv('OIDC_CLIENT_ID'),
        'client_secret': os.getenv('OIDC_CLIENT_SECRET')
    }
}```
