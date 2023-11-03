from openid.models import User

def create_user(userinfo, userdata):

    if User.objects.get(pk=userinfo['email']) == None:
        user = User(username=parts[1], password=make_password(parts[2]), first_name=parts[3], last_name=parts[4], email=parts[5], is_staff=parts[6])

        user.save()

    return