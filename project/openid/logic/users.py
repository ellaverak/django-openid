from openid.models import User

def create_user(userinfo, userdata):

    if User.objects.get(pk=userinfo['email']) is not None:
        return

    user = User(username=userinfo['uid'], first_name=userinfo['given_name'], last_name=userinfo['family_name'], email=userinfo['email'])

    user.save()